import os

import pika
from api.config import (
    rabbit_host,
    rabbit_password,
    rabbit_port,
    rabbit_queue,
    rabbit_username,
)
from api.tasks import celery_app
from flask import Flask, request


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        msg = f"""
        rabbit_host={rabbit_host}
        rabbit_port={rabbit_port}
        rabbit_username={rabbit_username}
        rabbit_password={rabbit_password}
        """
        return msg

    @app.route("/hello", methods=["GET"])
    def hello_world():
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_queue, durable=True)
        channel.basic_publish(
            exchange="", routing_key=rabbit_queue, body="Hello World!"
        )
        connection.close()
        return "Sent 'Hello World!'"

    @app.route("/publish", methods=["POST"])
    def publish_message():
        msg = request.data
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_queue, durable=True)
        channel.basic_publish(exchange="", routing_key=rabbit_queue, body=msg)
        connection.close()
        return msg

    @app.route("/task", methods=["POST"])
    def publish_task():
        msg = request.data
        task = celery_app.send_task(name="applications.celery-consumer.tasks.hello")
        return task

    return app
