# `uv` in Action

### Create a project
```bash
uv init --app
```

### Add dependencies
```bash
uv add ruff
uv add fastapi --extras standard
```

### Run the FastAPI server 
```bash
uv run fastapi dev 
```

### Make a request 
```bash
uv-in-action % http "127.0.0.1:8000/?token=jessica" 

HTTP/1.1 200 OK
content-length: 40
content-type: application/json
date: Wed, 11 Feb 2026 12:33:37 GMT
server: uvicorn

{
    "message": "Hello Bigger Applications!"
}
```
