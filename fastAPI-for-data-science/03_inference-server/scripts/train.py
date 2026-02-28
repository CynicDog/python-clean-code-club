import logging
import pathlib
import joblib
from datetime import datetime

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score


MODEL_DIR = pathlib.Path("models")
MODEL_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_data():
    logger.info("Loading Iris dataset...")
    data = load_iris()
    return data.data, data.target, data.target_names


def train_model():
    # Load and Split
    X, y, target_names = load_data()

    # Stratify ensures equal class distribution in both sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Define the Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42))
    ])

    # Training
    logger.info("Starting model training...")
    pipeline.fit(X_train, y_train)

    # Evaluation
    predictions = pipeline.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    logger.info(f"Model Accuracy: {acc:.4f}")
    logger.info("\n" + classification_report(y_test, predictions, target_names=target_names))

    # Serialization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    model_path = MODEL_DIR / f"iris_rf_v1_{timestamp}.pkl"
    latest_path = MODEL_DIR / "iris_model_latest.pkl"

    joblib.dump(pipeline, model_path)
    joblib.dump(pipeline, latest_path)

    logger.info(f"Model saved to {model_path}")


if __name__ == "__main__":
    try:
        train_model()
    except Exception as e:
        logger.error(f"Training failed: {e}")