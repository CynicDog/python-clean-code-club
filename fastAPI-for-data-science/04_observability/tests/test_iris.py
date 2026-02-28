import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient with the lifespan context.
    """
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    """
    Test the /health endpoint to ensure the model is loaded in state.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_prediction_success(client):
    """
    Test a valid prediction request.
    """
    payload = {"features": [5.1, 3.5, 1.4, 0.2]}
    response = client.post("/iris/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "predict" in data
    assert data["predict"]["species"] == "setosa"
    assert "model_version" in data
    assert "timestamp" in data


def test_prediction_invalid_data(client):
    """
    Test that the API returns 422 Unprocessable Entity for bad input.
    """
    payload = {"features": "not a list"}
    response = client.post("/iris/predict", json=payload)

    assert response.status_code == 422
