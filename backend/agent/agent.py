import random
import numpy as np
import torch
import torch.nn.functional as F
from collections import deque
from agent.network import QNetwork

class DQNAgent:
    def __init__(self, obs_dim, n_actions, lr, gamma, batch_size, buffer_capacity, l_actions_not_to_choose_randomly=[]):
        self.obs_dim = obs_dim
        self.n_actions = n_actions
        self.lr = lr
        self.gamma = gamma
        self.batch_size = batch_size
        self.buffer_capacity = buffer_capacity
        self.l_actions_not_to_choose_randomly = l_actions_not_to_choose_randomly

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_net = QNetwork(obs_dim, n_actions).to(self.device)
        self.target_net = QNetwork(obs_dim, n_actions).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = torch.optim.Adam(self.policy_net.parameters(), lr=lr)
        self.replay_buffer = deque(maxlen=buffer_capacity)

        self.last_action = None

    def select_action(self, state, epsilon):
        if random.random() < epsilon:
            while True:
                action = random.randint(0, self.n_actions - 1)

                if action not in self.l_actions_not_to_choose_randomly:
                    return action
        else:
            state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
            with torch.no_grad():
                q_values = self.policy_net(state).squeeze(0)
            
            if self.last_action is not None:
                face = self.last_action // 3

                q_values[face * 3] = -np.inf
                q_values[face * 3 + 1] = -np.inf
                q_values[face * 3 + 2] = -np.inf

            action = q_values.argmax().item()
            self.last_action = action

            return action

    def store_transition(self, transition):
        self.replay_buffer.append(transition)

    def update(self):
        if len(self.replay_buffer) < self.batch_size:
            return

        batch = random.sample(self.replay_buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(states, dtype=torch.float32).to(self.device)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1).to(self.device)
        next_states = torch.tensor(next_states, dtype=torch.float32).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1).to(self.device)

        q_values = self.policy_net(states).gather(1, actions)
        next_q_values = self.target_net(next_states).max(1)[0].unsqueeze(1)
        target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        loss = F.mse_loss(q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target_network(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def reset(self):
        self.last_action = None

