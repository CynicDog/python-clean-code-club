import contextlib
from fastapi import FastAPI
from pydantic import BaseModel

from src.inference.repository import ModelRepository
from src.inference.predict import predict


class IrisRequest(BaseModel):
    features: list[float]


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):

    repository = ModelRepository()

    app.state.model = repository.load_latest_model()

    print("model loaded")

    yield

    print("server shutting down")


app = FastAPI(
    title="Iris Torch API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict_endpoint(req: IrisRequest):

    model = app.state.model

    prediction = predict(model, req.features)

    return {"prediction": prediction[0]}
