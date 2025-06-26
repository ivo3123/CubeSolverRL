from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import torch
import numpy as np
from pathlib import Path
import sys
import os

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from agent.agent import DQNAgent
from cube_env.cube_env import RubiksCubeEnv
from cube.cube import get_solved_cube, move as apply_move
from cube.enums import Face, Rotation
from cube.utils import d_action_turn
from cube.scramble import generate_scramble

app = FastAPI(
    title="Rubik's Cube Solver API",
    description="API for solving Rubik's cubes using reinforcement learning",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for the agent and environment
agent: Optional[DQNAgent] = None
# env: Optional[RubiksCubeEnv] = None # No longer needed as global

# Pydantic models for request/response
class CubeState(BaseModel):
    state: List[int]  # Flattened cube state

class SolveRequest(BaseModel):
    cube_state: Optional[List[int]] = None  # If None, will use a random scramble
    max_moves: int = 100

class SolveResponse(BaseModel):
    success: bool
    moves: List[str]
    move_count: int
    final_state: List[int]
    message: str

class ScrambleResponse(BaseModel):
    scramble: List[str]
    cube_state: List[int]

def load_agent():
    """Load the trained agent model."""
    global agent
    
    # Load the best available model
    models_dir = backend_dir / "models"
    saved_models_dir = backend_dir / "saved_models" / "edges_first_layer"
    
    model_path = None
    # if models_dir.exists():
    #     if (models_dir / "model_edges_first_layer.pt").exists():
    #         print("1 EXISTSSSSSSSSSSS");
    #         model_path = models_dir / "model_edges_first_layer.pt"
    #     elif (models_dir / "1_edges_first_layer.pt").exists():
    #         print("2 EXISTSSSSSSSSSSS");
    #         model_path = models_dir / "1_edges_first_layer.pt"
    
    print("3 EXISTSSSSSSSSSSS");

    if model_path is None and saved_models_dir.exists():

        print("4 EXISTSSSSSSSSSSS");
        # Find the latest model in saved_models
        model_files = list(saved_models_dir.glob("model_*.pt"))
        if model_files:
            print("5 EXISTSSSSSSSSSSS");
            # Sort by the number in filename to get the latest
            model_files.sort(key=lambda x: int(x.stem.split('_')[-1]))
            model_path = model_files[-1]
    
    if model_path is None:
        raise FileNotFoundError("No trained model found. Please train a model first.")
    
    # Initialize agent with same parameters as training
    obs_dim = 54  # Flattened cube state
    n_actions = 18  # 6 faces * 3 rotations
    
    agent = DQNAgent(
        obs_dim=obs_dim,
        n_actions=n_actions,
        lr=0.001,  # Not used for inference
        gamma=0.99,  # Not used for inference
        batch_size=32,  # Not used for inference
        buffer_capacity=10000  # Not used for inference
    )
    
    # Load the trained weights
    agent.policy_net.load_state_dict(torch.load(model_path, map_location=agent.device))
    agent.policy_net.eval()
    
    print(f"Loaded model from: {model_path}")
    return agent

# This is no longer needed as we create envs on-demand
# def initialize_environment():
#     """Initialize the Rubik's cube environment."""
#     global env
#     env = RubiksCubeEnv(render_mode=None)
#     return env

@app.on_event("startup")
async def startup_event():
    """Initialize the agent and environment on startup."""
    try:
        load_agent()
        # initialize_environment() # Env is now created per-request
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        raise

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Rubik's Cube Solver API is running!"}

@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "agent_loaded": agent is not None,
        # "environment_loaded": env is not None, # Env is per-request
        "device": str(agent.device) if agent else "unknown"
    }

@app.post("/scramble", response_model=ScrambleResponse)
async def generate_cube_scramble(moves: int = 20):
    """Generate a scrambled cube state."""
    try:
        # Create a local environment for scrambling
        env = RubiksCubeEnv(render_mode=None, scramble_on_reset=False)
        
        # Apply random scramble
        scramble_moves_tuples = generate_scramble(moves)
        
        # Convert scramble moves to string format
        move_strings = []
        for face, rotation in scramble_moves_tuples:
            move_str = face.name
            if rotation == Rotation.CounterClockwise:
                move_str += "'"
            elif rotation == Rotation.Double:
                move_str += "2"
            move_strings.append(move_str)
        
        # Apply scramble to environment
        for face, rotation in scramble_moves_tuples:
            action = face.value * 3 + rotation.value
            env.step(action)
        
        return ScrambleResponse(
            scramble=move_strings,
            cube_state=env._get_obs().tolist()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating scramble: {str(e)}")

@app.post("/solve", response_model=SolveResponse)
async def solve_cube(request: SolveRequest):
    """Solve the Rubik's cube using the trained RL agent."""
    try:
        if agent is None:
            raise HTTPException(status_code=500, detail="Agent not initialized")
        
        # Create a local environment, ensure it starts in a solved state
        env = RubiksCubeEnv(render_mode=None, scramble_on_reset=False)
        
        # Set up the cube state
        if request.cube_state:
            # Use provided cube state
            try:
                env.set_state(request.cube_state)
            except (ValueError, IndexError) as e:
                raise HTTPException(status_code=400, detail=f"Invalid cube state provided: {e}")
            obs = env._get_obs()
        else:
            # Generate a random scramble by creating a temporary scrambled env
            scramble_env = RubiksCubeEnv(render_mode=None, scramble_on_reset=True)
            obs = scramble_env._get_obs()
            env.cube = scramble_env.cube # Copy the state to our main env
        
        # Solve the cube
        moves = []
        move_strings = []
        
        initial_state_is_solved = _is_solved(env.cube)

        for step in range(request.max_moves):
            if _is_solved(env.cube):
                 break

            # Get action from agent (greedy, no exploration)
            action = agent.select_action(obs, epsilon=0.0)  # No random actions
            
            # Convert action to move string
            face_idx = action // 3
            rotation_idx = action % 3
            
            face = Face(face_idx)
            rotation = Rotation(rotation_idx)
            
            move_str = face.name
            if rotation == Rotation.Clockwise:
                pass  # No suffix for clockwise
            elif rotation == Rotation.CounterClockwise:
                move_str += "'"
            elif rotation == Rotation.Double:
                move_str += "2"
            
            moves.append((face, rotation))
            move_strings.append(move_str)
            
            # Apply the move
            obs, reward, done, truncated, info = env.step(action)
            
            # The 'done' flag from the environment indicates the goal is reached
            if done:
                break

            print(f'Step {step}: move={move_str}, reward={reward}, done={done}')
        
        final_is_solved = _is_solved(env.cube)

        if final_is_solved:
             return SolveResponse(
                success=True,
                moves=move_strings,
                move_count=len(move_strings),
                final_state=obs.tolist(),
                message=f"Cube solved in {len(move_strings)} moves!" if not initial_state_is_solved else "Cube is already solved."
            )
        else:
            return SolveResponse(
                success=False,
                moves=move_strings,
                move_count=len(move_strings),
                final_state=obs.tolist(),
                message=f"Could not solve cube within {request.max_moves} moves."
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solving cube: {str(e)}")

def _is_solved(cube_state: dict):
    """Check if the cube is in solved state by comparing its dict representation."""
    return cube_state == get_solved_cube()

@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded model."""
    if agent is None:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    return {
        "device": str(agent.device),
        "observation_dim": agent.obs_dim,
        "action_count": agent.n_actions,
        "model_parameters": sum(p.numel() for p in agent.policy_net.parameters()),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
