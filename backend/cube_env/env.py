import gymnasium as gym
from gymnasium import spaces
import numpy as np
from cube.cube import move, get_solved_cube
from cube.enums import Face, Rotation
from cube.renderer import print_cube
from cube.enums import Letter, PieceType, Color
from cube_env.phases import count_solved_edges_first_layer, Phases
from cube.utils import d_action_turn
from cube.scramble import generate_scramble

class RubiksCubeEnv(gym.Env):
    """Custom Gymnasium environment for a Rubik's Cube."""

    def __init__(self, initial_scramble=None, render_mode="human", should_only_use_u_l_moves=False):
        super().__init__()

        rotations_count = 3
        faces_count = 2 if should_only_use_u_l_moves else 6
        available_moves_count = rotations_count * faces_count
        
        self.action_space = spaces.Discrete(available_moves_count)
        
        # Observation space: Cube state as a flattened array of colors
        # Each piece is encoded as its color value (0-5 for Color enum)
        self.observation_space = spaces.Box(
            low=0,
            high=5,
            shape=(54,),
            dtype=np.int8
        )
        
        self.initial_scramble = initial_scramble
        self.render_mode = render_mode
        self.should_only_use_u_l_moves = should_only_use_u_l_moves

        self.reset()

    def reset(self, seed=None, options=None):
        """Reset the cube to a solved state."""

        super().reset(seed=seed)
        self._apply_scramble()
        self.counter_for_punishment = 1

        self.edges_first_layer_solved_count = count_solved_edges_first_layer(self.cube)

        if self.edges_first_layer_solved_count < 4:
            self.current_phase = Phases.EdgesFirstLayer
        else:
            self.current_phase = Phases.CornersFirstLayer
            
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

        if self.current_phase == Phases.EdgesFirstLayer:
            prev_count = self.edges_first_layer_solved_count
            curr_count = count_solved_edges_first_layer(self.cube)
            delta = curr_count - prev_count

            if curr_count == 4:
                reward = 150
                self.current_phase = Phases.CornersFirstLayer
                terminated = True
            elif delta > 0:
                reward = 8 * delta
            elif delta < 0:
                reward = -15 * abs(delta)
            else:
                reward = -1

            self.edges_first_layer_solved_count = curr_count

        return self._get_obs(), reward, terminated, truncated, {"action": str(turn)}

    def render(self):
        """Render the cube state."""

        if self.render_mode == "human":
            print_cube(self.cube)

        return None
    
    def close(self):
        pass

    def _is_solved(self) -> bool:
        """Check if the cube is solved."""

        solved_cube = get_solved_cube()
        return self.cube == solved_cube
    
    def _get_obs(self) -> np.ndarray:
        """Convert the cube state to a numpy array observation."""

        def get_face(letter1, letter2, letter3, letter4, face):
            np_face_top_row = np.array([
                self.cube.get((letter1, PieceType.Corner)).value,
                self.cube.get((letter1, PieceType.Edge)).value,
                self.cube.get((letter2, PieceType.Corner)).value,
            ])

            np_face_middle_row = np.array([
                self.cube.get((letter4, PieceType.Edge)).value,
                self.cube.get((face, PieceType.Center)).value,
                self.cube.get((letter2, PieceType.Edge)).value,
            ])

            np_face_bottom_row = np.array([
                self.cube.get((letter4, PieceType.Corner)).value,
                self.cube.get((letter3, PieceType.Edge)).value,
                self.cube.get((letter3, PieceType.Corner)).value,
            ])

            np_face = np.array([
                np_face_top_row,
                np_face_middle_row,
                np_face_bottom_row,
            ])

            return np_face

        np_u_face = get_face(Letter.A, Letter.B, Letter.C, Letter.D, Face.U)
        np_l_face = get_face(Letter.E, Letter.F, Letter.G, Letter.H, Face.L)
        np_f_face = get_face(Letter.I, Letter.J, Letter.K, Letter.L, Face.F)
        np_r_face = get_face(Letter.M, Letter.N, Letter.O, Letter.P, Face.R)
        np_b_face = get_face(Letter.Q, Letter.R, Letter.S, Letter.T, Face.B)
        np_d_face = get_face(Letter.U, Letter.V, Letter.W, Letter.X, Face.D)

        np_cube = np.array([
            np_u_face,
            np_l_face,
            np_f_face,
            np_r_face,
            np_b_face,
            np_d_face,
        ])

        return np_cube.flatten()

    def _apply_scramble(self) -> None:
        if self.initial_scramble is None:
            # self.initial_scramble = [
            #     (Face.R, Rotation.Clockwise),
            #     (Face.B, Rotation.CounterClockwise),
            #     (Face.L, Rotation.Clockwise),
            #     (Face.F, Rotation.Clockwise),
            #     (Face.L, Rotation.Double),
            #     (Face.U, Rotation.CounterClockwise),
            #     (Face.D, Rotation.Clockwise),
            #     (Face.B, Rotation.CounterClockwise),
            #     (Face.L, Rotation.Clockwise),
            #     (Face.B, Rotation.CounterClockwise),
            #     (Face.L, Rotation.Clockwise),
            #     (Face.F, Rotation.Clockwise),
            #     (Face.L, Rotation.Double),
            #     (Face.U, Rotation.CounterClockwise),
            #     (Face.D, Rotation.Clockwise),
            #     (Face.B, Rotation.CounterClockwise),
            #     (Face.L, Rotation.Clockwise),
            #     (Face.B, Rotation.CounterClockwise),
            # ]

            scramble = generate_scramble()
        
        self.cube = move(get_solved_cube(), l_turns=scramble)