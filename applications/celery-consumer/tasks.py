import os

from celery import Celery

rabbit_host = os.environ.get("RABBIT_HOST")
rabbit_port = os.environ.get("RABBIT_PORT")
rabbit_username = os.environ.get("RABBIT_USERNAME")
rabbit_password = os.environ.get("RABBIT_PASSWORD")
rabbit_queue = os.environ.get("RABBIT_QUEUE", "hello")

app = Celery("main", broker=f"amqp://{rabbit_username}@{rabbit_host}")


@app.task
def hello():
    return "hello world"
