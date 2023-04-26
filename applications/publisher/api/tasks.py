from api.config import rabbit_host, rabbit_username
from celery import Celery

celery_app = Celery("tasks", broker=f"amqp://{rabbit_username}@{rabbit_host}")
