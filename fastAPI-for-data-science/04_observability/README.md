# FastAPI for Data Science: Inference Server

### Create the Project
```bash
uv init --app
````

### Install Dependencies

```bash
uv add ruff
uv add fastapi --extra standard
uv add --dev pytest-asyncio httpx
uv add opentelemetry-api \
       opentelemetry-sdk \
       opentelemetry-instrumentation-fastapi \
       opentelemetry-exporter-otlp \
       opentelemetry-exporter-prometheus \
       prometheus-client       
```

### Run the FastAPI Server

```bash
uv run fastapi dev
```

### Train the model 
```bash 
uv run scripts/train.py 
```

### Run Tests

```bash
uv run pytest
```

### Run Linter

```bash
uv run ruff check .
```

## Run as Container

### Pull Image

```bash
docker pull ghcr.io/cynicdog/python-clean-code-club/iris-inference:latest

```

### Run Container

```bash
docker run -d -p 8000:80 --name iris-app ghcr.io/cynicdog/python-clean-code-club/iris-inference:latest

```

### Make Request

```bash
http POST :8000/iris/predict features:='[5.1, 3.5, 1.4, 0.2]'

```

### Run the Jaeger container 
```
docker run --rm -d --name jaeger \
  -p 16686:16686 \
  -p 4317:4317 \
  jaegertracing/all-in-one:latest
```
> - `16686`: The Web UI 
> - `4317` : The OTLP gRPC receiver


```
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

```
docker run -d --name grafana \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  grafana/grafana
```
