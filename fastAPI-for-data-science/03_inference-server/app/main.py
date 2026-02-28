import contextlib
from fastapi import FastAPI, Request
from .router import iris
from .repository.model import ModelRepository


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    repository = ModelRepository()
    app.state.model = repository.load_latest_model()
    yield


app = FastAPI(title="Iris Inference API", lifespan=lifespan)

app.include_router(iris.router)


@app.get("/health")
def health_check(request: Request):
    model_ready = (
        hasattr(request.app.state, "model") and request.app.state.model is not None
    )
    return {
        "status": "healthy" if model_ready else "unhealthy",
        "model_loaded": model_ready,
    }
