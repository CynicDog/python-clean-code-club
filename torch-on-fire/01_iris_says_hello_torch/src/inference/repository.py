import torch
from pathlib import Path

from src.models.mlp import IrisMLP


class ModelRepository:
    def __init__(self, artifact_dir: str = "artifacts"):
        self.artifact_dir = Path(artifact_dir)

    def load_latest_model(self):

        model_path = self.artifact_dir / "model.pt"

        model = IrisMLP()
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
        model.eval()

        return model
