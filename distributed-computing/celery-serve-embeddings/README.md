# Celery Serves Embeddings! 

### Start the Redis backend/broker container  
```bash
docker compose up 
```

#### Trigger the Task 
```bash 
http POST http://localhost:8000/ai/embed text="AI is the new electricity."
```

#### Check the result 
```bash
http GET http://localhost:8000/ai/result/{TASK_ID}
```