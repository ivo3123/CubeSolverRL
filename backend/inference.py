import torch
import numpy as np
from cube_env.cube_env import RubiksCubeEnv
from agent.agent import DQNAgent
from cube_env.phases import count_solved_edges_first_layer
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from cube.utils import d_action_turn

model_path = "models/1_edges_first_layer.pt"
obs_size = 54
n_actions = 18

agent = DQNAgent(
    obs_dim=obs_size,
    n_actions=n_actions,
    lr=1e-3,
    gamma=0.99,
    batch_size=64,
    buffer_capacity=10_000
)

agent.policy_net.load_state_dict(torch.load(model_path))
agent.policy_net.eval()

env = RubiksCubeEnv()

num_eval_episodes = 3
max_steps = 100

obs, _ = env.reset()

l_episodes = []
l_l_actions = []

for episode in range(1, num_eval_episodes+1):
    l_actions = []
    obs, _ = env.reset()
    done = False
    steps = 0
    total_reward = 0
    while not done and steps < max_steps:
        action = agent.select_action(obs, epsilon=0.00)
        l_actions.append(action)
        obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        total_reward += reward
        steps += 1

    solved = count_solved_edges_first_layer(env.cube) == 4
    # print(f"Solved edges: {count_solved_edges_first_layer(env.cube)} | Steps: {steps} | Total reward: {total_reward:.2f}")
    # print(l_actions)

    if done == False:
        print("PANIK")

    env.render()
    l_episodes.append(episode)
    l_l_actions.append(l_actions)

env.close()

pl_data = pl.DataFrame({
    "episodes": l_episodes,
    "actions": l_l_actions,
})\
    .with_columns(
        pl.col("actions").list.len().alias("moves_count"),
    )\
    .with_columns(
        pl.col("moves_count").mean().alias("mean"),
        pl.col("moves_count").std().alias("std"),
    )

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=pl_data["episodes"],
        y=pl_data["moves_count"],
        name="Moves count"
    )
)

fig.add_trace(
    go.Scatter(
        x=pl_data["episodes"],
        y=pl_data["mean"],
        name="Mean moves count",
        line=dict(dash='dash')
    )
)

fig.update_layout(
    height=650,
    title={
        'text': f'Moves count for solving edges of the first layer in inference',
        'x': 0.5,
        'y': 0.94,
    },
    xaxis=dict(title='Episode'),
    yaxis=dict(title='Moves count'),
)

fig.show()