import gymnasium as gym
from gymnasium import spaces
import numpy as np
from cube.cube import move, get_solved_cube
from cube.enums import Face, Rotation
from cube.renderer import print_cube

class RubiksCubeEnv(gym.Env):
    """Custom Gymnasium environment for a Rubik's Cube."""

    def __init__(self, render_mode):
        super().__init__()
        
        self.action_space = spaces.Discrete(18)  # (6 faces × 3 rotations)
        
        # Observation space: Cube state as a flattened array of colors
        # Each piece is encoded as its color value (0-5 for Color enum)
        self.observation_space = spaces.Box(
            low=0,
            high=5,
            shape=(54,),
            dtype=np.int8
        )
        
        self.cube = get_solved_cube()
        self.render_mode = render_mode

    def _get_obs(self) -> np.ndarray:
        """Convert the cube state to a numpy array observation."""

        obs = np.zeros(54, dtype=np.int8)
        # Map each cube piece to a unique index (simplified example)
        for idx, ((letter, piece_type), color) in enumerate(self.cube.items()):
            obs[idx] = color.value
        return obs

    def reset(self, seed=None, options=None):
        """Reset the cube to a solved state."""

        super().reset(seed=seed)
        self.cube = get_solved_cube()
        return self._get_obs(), {"info": "Cube reset to solved state."}

    def step(self, action: int):
        """Execute a move and return (obs, reward, terminated, truncated, info)."""

        # Map action to (Face, Rotation)
        face = Face(action // 3)  # 0-5 for faces
        rotation = Rotation(action % 3)  # 0-2 for rotations
        
        self.cube = move(self.cube, [(face, rotation)])
        
        terminated = self._is_solved()
        reward = 1.0 if terminated else -0.01
        
        return (
            self._get_obs(),
            reward,
            terminated,
            False,  # Truncated (not used here)
            {"action": f"{face.name} {rotation.name}"},
        )

    def _is_solved(self) -> bool:
        """Check if the cube is solved."""

        solved_cube = get_solved_cube()
        return self.cube == solved_cube

    def render(self):
        """Render the cube state."""

        if self.render_mode == "console":
            print_cube(self.cube)

        return None
    