# FastAPI for Data Science: Realtime Server

### Create the Project
```bash
uv init --app
````

### Install Dependencies

```bash
uv add ruff
uv add fastapi --extras standard
uv add --dev pytest-asyncio 
```

### Run the FastAPI Server

```bash
uv run uvicorn app.main:app --reload
uv run python -m http.server --directory app 9000
```

### Run Tests

```bash
uv run pytest
```

### Run Linter

```bash
uv run ruff check .
```

### Run Redis Server (Docker)

```bash
docker run -d --name fastapi-redis \
  -p 6379:6379 \
  redis
```
