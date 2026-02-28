# FastAPI for Data Science: API Server

### Create the Project
```bash
uv init --app
````

### Install Dependencies

```bash
uv add ruff
uv add fastapi --extra standard
uv add "sqlalchemy[asyncio]"
uv add asyncpg
uv add --dev pytest-asyncio httpx aiosqlite
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

### Run Postgres Database (Docker)

```bash
docker run -d --name fastapi-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fastapi_db \
  -p 5432:5432 \
  postgres:16
```
