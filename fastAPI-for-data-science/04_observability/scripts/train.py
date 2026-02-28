import logging
import pathlib
from datetime import datetime

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

from skl2onnx.common.data_types import FloatTensorType
from skl2onnx import to_onnx
import onnxruntime as rt

MODEL_DIR = pathlib.Path("models")
MODEL_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_data():
    logger.info("Loading Iris dataset...")
    data = load_iris()
    return data.data, data.target, data.target_names


def train_model():
    X, y, target_names = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
            ),
        ]
    )

    logger.info("Starting model training...")
    pipeline.fit(X_train, y_train)

    # Scikit-learn Evaluation
    sk_predictions = pipeline.predict(X_test)
    acc = accuracy_score(y_test, sk_predictions)
    logger.info(f"Model Accuracy (SKLearn): {acc:.4f}")
    logger.info(
        "\n" + classification_report(y_test, sk_predictions, target_names=target_names)
    )

    logger.info("Converting model to ONNX format...")

    initial_type = [("float_input", FloatTensorType([None, 4]))]

    onx = to_onnx(pipeline, initial_types=initial_type)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    onnx_versioned_path = MODEL_DIR / f"iris_rf_v1_{timestamp}.onnx"
    onnx_latest_path = MODEL_DIR / "iris_model_latest.onnx"

    with open(onnx_versioned_path, "wb") as f:
        f.write(onx.SerializeToString())
    with open(onnx_latest_path, "wb") as f:
        f.write(onx.SerializeToString())

    logger.info("Verifying ONNX model output matches SKLearn...")
    sess = rt.InferenceSession(str(onnx_latest_path))
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name

    onnx_pred = sess.run([label_name], {input_name: X_test.astype(np.float32)})[0]

    if np.allclose(sk_predictions, onnx_pred):
        logger.info("Verification Success: ONNX and SKLearn outputs match!")
    else:
        logger.warning(
            "Verification Warning: ONNX and SKLearn outputs differ slightly."
        )

    logger.info(f"Model saved to {onnx_versioned_path}")


if __name__ == "__main__":
    try:
        train_model()
    except Exception as e:
        logger.error(f"Training failed: {e}", exc_info=True)
