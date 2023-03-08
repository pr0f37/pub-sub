import os

import pika
from flask import Flask, request


def create_app():
    app = Flask(__name__)
    rabbit_host = os.environ.get("RABBIT_HOST")
    rabbit_port = os.environ.get("RABBIT_PORT")
    rabbit_username = os.environ.get("RABBIT_USERNAME")
    rabbit_password = os.environ.get("RABBIT_PASSWORD")
    rabbit_queue = os.environ.get("RABBIT_QUEUE", "hello")

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

    return app
