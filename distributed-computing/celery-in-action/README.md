# Celery in Action 

### Start the Redis backend/broker container  
```bash
docker run -d -p 6379:6379 redis
```

### Start the Celery Worker 
```bash
uv run celery -A app.internal.worker.celery_app worker --loglevel=info
```

### Start FastAPI server 
```bash
uv run fastapi dev
```

#### Trigger the Task 
```bash 
http POST 'http://localhost:8000/tasks/add?x=15&y=25'
```

#### Check the result 
```bash
http GET http://localhost:8000/tasks/result/{TASK_ID}
```