import os
from celery import Celery

celery = Celery(
    "farmer_app",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=True
)