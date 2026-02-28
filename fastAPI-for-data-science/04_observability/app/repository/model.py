import onnxruntime as rt
from pathlib import Path


class ModelRepository:
    def __init__(self, model_path: str = "models/iris_model_latest.onnx"):
        self.path = Path(model_path)

    def load_latest_model(self):
        if not self.path.exists():
            raise FileNotFoundError(f"Model artifact not found at {self.path}")

        return rt.InferenceSession(str(self.path))
