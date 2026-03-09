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

### Run as Container

```bash
docker run -d -p 8000:80 --name ghcr.io/cynicdog/python-clean-code-club/fastapi-for-data-science:api-server  
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

## ps. Docker image is essentially packaged filesystem as a file on disk 

```bash 
docker save -o fastapi-image.tar ghcr.io/cynicdog/python-clean-code-club/fastapi-for-data-science:api-server
ls -lh fastapi-image.tar
tar -tf fastapi-image.tar 

mkdir fastapi-image
tar -xf fastapi-image.tar -C fastapi-image
cd fastapi-image
tree 
```
