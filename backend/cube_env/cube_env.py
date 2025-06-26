import gymnasium as gym
from gymnasium import spaces
import numpy as np
from cube.cube import move, get_solved_cube
from cube.enums import Face, Rotation
from cube.renderer import print_cube
from cube.enums import Letter, PieceType, Color
from cube_env.phases import count_solved_edges_first_layer, count_solved_corners_first_layer, Phases
from cube.utils import d_action_turn, transform_into_numpy_array
from cube.scramble import generate_scramble

class RubiksCubeEnv(gym.Env):
    """Custom Gymnasium environment for a Rubik's Cube."""

    def __init__(
        self,
        initial_scramble=None,
        render_mode="human",
        solving_phase: Phases = Phases.EdgesFirstLayer,
    ):
        super().__init__()
        
        # 18 turns, look d_action_turn
        self.action_space = spaces.Discrete(18)
        
        # 54 stickers on a cube each with a color value (0-6 for Color enum)
        self.observation_space = spaces.Box(
            low=0,
            high=6,
            shape=(54,),
            dtype=np.int8
        )
        
        self.initial_scramble = initial_scramble
        self.render_mode = render_mode
        self.solving_phase = solving_phase

        self.reset()

    def reset(self, seed=None, options=None):
        """Reset the cube to a solved state."""

        super().reset(seed=seed)
        self._apply_scramble()

        self.edges_first_layer_solved_count = count_solved_edges_first_layer(self.cube)
        self.corners_first_layer_solved_count = count_solved_corners_first_layer(self.cube)

        self.corners_first_layer_solved_count = count_solved_corners_first_layer(self.cube)

        return self._get_obs(), {"info": "Cube reset to solved state."}

    def step(self, action: int):
        """Execute a move and return (obs, reward, terminated, truncated, info)."""

        """
            note this action to turn mapping is the same as

            face = Face(action // 3)
            rotation = Rotation(action % 3)

            the more explicit variant is used for more clarity in the code
        """
        
        turn = d_action_turn[action]
        self.cube = move(self.cube, turn)

        reward = 0.0
        terminated = False
        truncated = False

        if self.solving_phase == Phases.EdgesFirstLayer:
            edges_first_layer_solved_count_before_turn = self.edges_first_layer_solved_count
            edges_first_layer_solved_count_after_turn = count_solved_edges_first_layer(self.cube)

            self.edges_first_layer_solved_count = edges_first_layer_solved_count_after_turn

            delta = edges_first_layer_solved_count_after_turn - edges_first_layer_solved_count_before_turn
            if edges_first_layer_solved_count_after_turn == 4:
                reward += 50
                terminated = True
            elif delta != 0:
                reward += 10 * delta
            elif delta == 0:
                reward += -0.2

        if self.solving_phase == Phases.CornersFirstLayer:
            edges_first_layer_solved_count_before_turn = self.edges_first_layer_solved_count
            edges_first_layer_solved_count_after_turn = count_solved_edges_first_layer(self.cube)

            corners_first_layer_solved_count_before_turn = self.corners_first_layer_solved_count
            corners_first_layer_solved_count_after_turn = count_solved_corners_first_layer(self.cube)

            if edges_first_layer_solved_count_after_turn == 4:
                self.corners_first_layer_solved_count = corners_first_layer_solved_count_after_turn

                delta = corners_first_layer_solved_count_after_turn - corners_first_layer_solved_count_before_turn
                if corners_first_layer_solved_count_after_turn == 4:
                    reward += 150
                    terminated = True
                elif delta != 0:
                    reward += 20 * delta
                elif delta == 0:
                    reward += 0
            elif edges_first_layer_solved_count_after_turn == 3:
                reward += -1
            elif edges_first_layer_solved_count_after_turn < 3:
                reward += -10

            self.edges_first_layer_solved_count = edges_first_layer_solved_count_after_turn

        return self._get_obs(), reward, terminated, truncated, {"action": str(turn)}

    def render(self):
        """Render the cube state."""

        if self.render_mode == "human":
            print_cube(self.cube)

        return None
    
    def close(self):
        pass
    
    def _get_obs(self) -> np.ndarray:
        """Convert the cube state to a numpy array observation."""

        if self.solving_phase == Phases.EdgesFirstLayer:
            should_consider_edges_first_layer = True
            should_consider_corners_first_layer = False
            should_consider_edges_second_layer = False
            should_consider_edges_third_layer = False
            should_consider_corners_third_layer = False
        elif self.solving_phase == Phases.CornersFirstLayer:
            should_consider_edges_first_layer = True
            should_consider_corners_first_layer = True
            should_consider_edges_second_layer = False
            should_consider_edges_third_layer = False
            should_consider_corners_third_layer = False
        elif self.solving_phase == Phases.EdgesSecondLayer:
            should_consider_edges_first_layer = True
            should_consider_corners_first_layer = True
            should_consider_edges_second_layer = True
            should_consider_edges_third_layer = False
            should_consider_corners_third_layer = False

        np_matrix = transform_into_numpy_array(
            self.cube,
            should_consider_edges_first_layer = should_consider_edges_first_layer,
            should_consider_corners_first_layer = should_consider_corners_first_layer,
            should_consider_edges_second_layer = should_consider_edges_second_layer,
            should_consider_edges_third_layer = should_consider_edges_third_layer,
            should_consider_corners_third_layer = should_consider_corners_third_layer,
        )

        return np_matrix.flatten()

    def _apply_scramble(self) -> None:
        if self.initial_scramble is None:
            scramble = generate_scramble()
        
        self.cube = move(get_solved_cube(), l_turns=scramble)