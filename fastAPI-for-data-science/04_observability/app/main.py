import os
import contextlib

from fastapi import FastAPI, Request

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

from .router import iris
from .repository.model import ModelRepository

otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
service_name = os.getenv("OTEL_SERVICE_NAME", "iris-inference-service")

resource = Resource.create({"service.name": service_name})

trace_provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=True)

trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(trace_provider)

metric_reader = PrometheusMetricReader()
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)


start_http_server(port=9464)


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
