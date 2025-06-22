import torch
import numpy as np
from cube_env.env import RubiksCubeEnv
from agent.agent import DQNAgent
from cube_env.phases import count_solved_edges_first_layer
import polars as pl
import plotly.express as px
from cube.utils import d_action_turn

num_episodes = 2_000
max_steps = 72
gamma = 0.99
epsilon_start = 1.0
epsilon_end = 0.09
epsilon_decay = 0.999
learning_rate = 0.0005
batch_size = 64
buffer_capacity = 10_000
target_update_interval = 10

env = RubiksCubeEnv()
obs_size = env.observation_space.shape[0]
n_actions = env.action_space.n

agent = DQNAgent(
    obs_dim=obs_size,
    n_actions=n_actions,
    lr=learning_rate,
    gamma=gamma,
    batch_size=batch_size,
    buffer_capacity=buffer_capacity
)

epsilon = epsilon_start

l_episodes = []
l_rewards = []
l_epsilons = []
l_edges_solved_count = []
l_l_actions = []

for episode in range(num_episodes):
    obs, _ = env.reset()
    total_reward = 0

    l_actions = []

    for step in range(max_steps):
        action = agent.select_action(obs, epsilon)
        l_actions.append(action)
        next_obs, reward, terminated, truncated, _ = env.step(action)

        done = terminated or truncated
        agent.store_transition((obs, action, reward, next_obs, done))
        agent.update()

        obs = next_obs
        total_reward += reward

        if done:
            break

    if episode % target_update_interval == 0:
        agent.update_target_network()

    epsilon = max(epsilon * epsilon_decay, epsilon_end)

    l_epsilons.append(epsilon)
    l_rewards.append(total_reward)
    l_episodes.append(episode)
    l_edges_solved_count.append(count_solved_edges_first_layer(env.cube))
    l_l_actions.append(l_actions)

    print(f"Ep {episode} | Reward: {total_reward:.2f} | Epsilon: {epsilon:.3f} | Edges solve: {count_solved_edges_first_layer(env.cube)}")

    if episode % 100 == 0:
        torch.save(agent.policy_net.state_dict(), f"saved_models/edges_first_layer/model_{episode}.pt")

env.close()

torch.save(agent.policy_net.state_dict(), "saved_models/edges_first_layer/model.pt")

pl_data = pl.DataFrame({
    "episode": l_episodes,
    "reward": l_rewards,
    "epsilon": l_epsilons,
    "edges_solved": l_edges_solved_count,
    "actions": l_l_actions,
})\
    .with_columns(
        pl.col("reward").rolling_mean(100).alias("reward_rolling_mean"),
        pl.col("edges_solved").rolling_mean(100).alias("edges_solved_mean"),
        pl.col("edges_solved").rolling_median(50).alias("edges_solved_median"),
    )

fig = px.line(pl_data, x="episode", y=["reward", "epsilon", "edges_solved", "reward_rolling_mean", "edges_solved_mean", "edges_solved_median"])

fig.update_layout(
    height=575,
)

fig.show()