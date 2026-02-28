import contextlib
from fastapi import FastAPI, Request

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .router import iris
from .repository.model import ModelRepository


resource = Resource.create({"service.name": "iris-inference-service"})
provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)

processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    repository = ModelRepository()
    app.state.model = repository.load_latest_model()
    yield

app = FastAPI(title="Iris Inference API", lifespan=lifespan)

app.include_router(iris.router)

FastAPIInstrumentor.instrument_app(app)


@app.get("/health")
def health_check(request: Request):
    model_ready = (
        hasattr(request.app.state, "model") and request.app.state.model is not None
    )
    return {
        "status": "healthy" if model_ready else "unhealthy",
        "model_loaded": model_ready,
    }