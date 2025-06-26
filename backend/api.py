from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cube.enums import Face, Rotation
from cube_env.cube_env import RubiksCubeEnv
from cube.utils import d_action_turn, d_face_str, d_rotation_str
from agent.ready_agents import get_agent_for_edges_first_layer

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # to try substitution with ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/solve")
def solve_cube():
    agent = get_agent_for_edges_first_layer()

    initial_scramble = [
        (Face.R, Rotation.Double),
        (Face.U, Rotation.Double),
        (Face.F, Rotation.Clockwise),
        (Face.L, Rotation.CounterClockwise),
        (Face.D, Rotation.Double),
        (Face.B, Rotation.Clockwise),
        (Face.R, Rotation.CounterClockwise),
        (Face.D, Rotation.CounterClockwise),
        (Face.L, Rotation.Clockwise),
        (Face.F, Rotation.Double),
        (Face.U, Rotation.CounterClockwise),
        (Face.B, Rotation.Double),
    ]

    env = RubiksCubeEnv(initial_scramble=initial_scramble)
    obs, _ = env.reset()
    done = False
    turns = []
    steps = 0

    while not done and steps < 100:
        action = agent.select_action(obs, epsilon=0.0)
        obs, _, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        turns.append(d_action_turn[action])
        steps += 1

    actions = []
    for turn in turns:
        face, rotation = turn
        actions.append(d_face_str[face] + d_rotation_str[rotation])

    return {"moves": actions}