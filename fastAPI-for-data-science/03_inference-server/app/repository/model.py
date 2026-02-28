import joblib
from pathlib import Path


class ModelRepository:
    def __init__(self, model_path: str = "models/iris_model_latest.pkl"):
        self.path = Path(model_path)

    def load_latest_model(self):
        if not self.path.exists():
            raise FileNotFoundError(f"Model artifact not found at {self.path}")
        return joblib.load(self.path)
