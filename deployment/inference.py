import os
import torch
from model_def import Linear_QNet

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "training", "model", "model.pth")

class SnakeAgent:
    def __init__(self):
        self.model = Linear_QNet(11, 256, 3)
        self.model.load_state_dict(
            torch.load(MODEL_PATH, map_location="cpu")
        )
        self.model.eval()

    def act(self, state):
        state = torch.tensor(state, dtype=torch.float)
        with torch.no_grad():
            return torch.argmax(self.model(state)).item()
