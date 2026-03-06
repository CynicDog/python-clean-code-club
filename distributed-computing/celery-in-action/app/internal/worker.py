"""Celery worker module for background task processing."""

import time
import os

from celery import Celery

REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)


@celery_app.task(name="app.internal.worker.add_task")
def add_task(x: int, y: int):
    """Adds two integers together after a simulated delay.

    Args:
        x: The first integer to add.
        y: The second integer to add.

    Returns:
        The sum of x and y.
    """
    time.sleep(5)
    return x + y
