# Iris Says Hello, Torch!

Minimal clean-code PyTorch example with training, testing, and a FastAPI inference server.

## Setup

Install dependencies:

```bash
uv sync
```

## Run train

```bash
uv run python main.py
```

### Optional: override config via environment variables.
```bash 
BATCH_SIZE=128 EPOCHS=50 LR=0.0005 uv run python main.py
```

## Run tests

```bash
uv run pytest
```

## Run online inference server

```bash
uv run uvicorn src.inference.app:app --reload
```

## Request example

```bash
http POST http://localhost:8000/predict features:='[5.1,3.5,1.4,0.2]'

HTTP/1.1 200 OK
content-length: 16
content-type: application/json
date: Tue, 10 Mar 2026 11:53:58 GMT
server: uvicorn

{
    "prediction": 0
}
```
