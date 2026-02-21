# FastAPI for Data Science 

### Create a project
```bash
uv init --app
```

### Install Dependencies
```
uv add ruff
uv add fastapi --extras standard
uv add "sqlalchemy[asyncio,mypy]"
uv add asyncpg
```

### Run the FastAPI server 
```bash
uv run fastapi dev 
```

### Run Postgres Database
```bash 
docker run -d --name fastapi-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fastapi_db \
  -p 5432:5432 \
  postgres:16
```

### Run MongoDB Database
```bash 
docker run -d --name fastapi-mongo \
  -p 27017:27017 \
  mongo:6.0
```

