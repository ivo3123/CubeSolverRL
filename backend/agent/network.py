import torch
import torch.nn as nn

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        size = 512

        self.net = nn.Sequential(
            nn.Linear(state_size, size),
            nn.ReLU(),
            nn.Linear(size, size),
            nn.LeakyReLU(),
            nn.Linear(size, action_size)
        )
        self.to(self.device)

    def forward(self, x):
        return self.net(x)