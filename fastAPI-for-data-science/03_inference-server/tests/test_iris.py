import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.router.iris import get_prediction_service

from app.dto.iris import (
    IrisPredictResponse,
    PredictionResult,
    IrisFeatures,
)


class DummyPredictionService:
    def __init__(self, model=None):
        self.model = model

    def predict(self, request):
        return IrisPredictResponse(
            predict=PredictionResult(
                species="setosa",
                probability=0.99,
            ),
            feed=[
                IrisFeatures(
                    sepal_length=request.features[0],
                    sepal_width=request.features[1],
                    petal_length=request.features[2],
                    petal_width=request.features[3],
                )
            ],
            model_version="rf_v1",
        )


@pytest.fixture
def client():
    app.dependency_overrides[get_prediction_service] = lambda: DummyPredictionService()

    with TestClient(app) as client:
        yield client

    app.dependency_overrides = {}


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in ["healthy", "unhealthy"]
    assert "model_loaded" in response.json()


def test_predict_success(client):
    payload = {"features": [5.1, 3.5, 1.4, 0.2]}

    response = client.post("/iris/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["predict"]["species"] == "setosa"
    assert data["predict"]["probability"] == 0.99
    assert data["model_version"] == "rf_v1"
    assert "timestamp" in data
    assert len(data["feed"]) == 1


def test_predict_invalid_input(client):
    payload = {"features": [5.1, 3.5]}

    response = client.post("/iris/predict", json=payload)

    assert response.status_code == 422
