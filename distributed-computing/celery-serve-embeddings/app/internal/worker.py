"""Celery configuration and Transformer tasks."""

import os
import logging
from celery import Celery, Task
from sentence_transformers import SentenceTransformer

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)


class EmbeddingTask(Task):
    """Base class to load the Transformer model once per worker process."""

    _model = None

    @property
    def model(self):
        """Lazy-loads the Transformer model and caches it in memory.

        This property ensures the model is only loaded once per worker process
        to optimize memory usage and inference speed.

        Returns:
            SentenceTransformer: The loaded all-MiniLM-L6-v2 model instance.
        """
        if self._model is None:
            logging.info("Loading Transformer Model: all-MiniLM-L6-v2...")
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            logging.info("Model loaded successfully.")
        return self._model


@celery_app.task(
    bind=True, base=EmbeddingTask, name="app.internal.worker.generate_embedding"
)
def generate_embedding(self, text: str):
    """Converts a string of text into a vector embedding list."""
    try:
        embedding = self.model.encode(text)
        return {"status": "SUCCESS", "result": embedding.tolist()}
    except Exception as e:
        logging.error(f"Embedding failed: {e}")
        return {"status": "FAIL", "result": str(e)}
