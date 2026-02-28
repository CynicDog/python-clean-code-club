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

```bash 
docker compose up 
``` 

### Setup Grafana

- Login to http://localhost:3000 (admin/admin)
- Go to Connections > Data Sources
- Click Add data source > Prometheus
- For the URL, enter: http://prometheus:9090
- Click Save & Test.

### Simulate requests 
```
uv run scripts/simulate_requests.py
```

### Grafana Dashboard 
<img width="1955" height="2115" alt="Screenshot 2026-02-28 at 8 46 30 PM" src="https://github.com/user-attachments/assets/b3844923-005a-4558-b666-d36fd6bb9b74" />

