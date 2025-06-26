import torch
from agent.agent import DQNAgent

def get_agent(model_path):
    agent = DQNAgent(
        obs_dim=54,
        n_actions=18,
        lr=1e-3,
        gamma=0.99,
        batch_size=64,
        buffer_capacity=10_000
    )

    agent.policy_net.load_state_dict(torch.load(model_path))
    agent.policy_net.eval()

    return agent

def get_agent_for_edges_first_layer():
    model_path = "models/1_edges_first_layer.pt"

    agent = get_agent(model_path)

    return agent