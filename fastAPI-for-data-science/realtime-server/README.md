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
uv run fastapi dev
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
