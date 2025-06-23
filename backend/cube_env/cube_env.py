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

        # if solving_phase == Phases.CornersFirstLayer:
        #     self.agent_edges_first_layer = self._make_agent("models/model_edges_first_layer.pt")

        self.reset()

    def reset(self, seed=None, options=None):
        """Reset the cube to a solved state."""

        super().reset(seed=seed)
        self._apply_scramble()

        self.edges_first_layer_solved_count = count_solved_edges_first_layer(self.cube)

        # if self.solving_phase != Phases.EdgesFirstLayer:
        #     assert self.edges_first_layer_solved_count == 4, "Expected correct envoirnmet"
            # if self.edges_first_layer_solved_count < 4:
            #     done = False
            #     steps = 0
            #     max_steps = 60
            #     while not done and steps < max_steps:
            #         obs = self._get_obs()
            #         action = agent.select_action(obs, epsilon=0.00)
            #         obs, reward, terminated, truncated, _ = env.step(action)
            #         done = terminated or truncated
            #         total_reward += reward
            #         steps += 1
            # else:
            #     pass

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
            prev_count = self.edges_first_layer_solved_count
            curr_count = count_solved_edges_first_layer(self.cube)
            delta = curr_count - prev_count
            if curr_count == 4:
                reward += 50
                terminated = True
            elif delta != 0:
                reward += 10 * delta
            elif delta == 0:
                reward += -0.2

            self.edges_first_layer_solved_count = curr_count

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

        np_matrix = transform_into_numpy_array(
            self.cube,
                should_consider_edges_first_layer = True,
                should_consider_corners_first_layer = False,
                should_consider_edges_second_layer = True,
                should_consider_edges_third_layer = True,
                should_consider_corners_third_layer = False,
        )

        return np_matrix.flatten()

    def _apply_scramble(self) -> None:
        if self.initial_scramble is None:
            scramble = generate_scramble()
        
        self.cube = move(get_solved_cube(), l_turns=scramble)

    # def _make_agent(self, path_to_model: str):
    #     n_actions = 18
    #     obs_size = 54

    #     agent = DQNAgent(
    #         obs_dim=obs_size,
    #         n_actions=n_actions,
    #         lr=1e-3,
    #         gamma=0.99,
    #         batch_size=64,
    #         buffer_capacity=10_000
    #     )

    #     agent.policy_net.load_state_dict(torch.load(model_path))
    #     agent.policy_net.eval()

    #     return agent