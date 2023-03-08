import json
import os
import time

import pika

rabbit_host = os.environ.get("RABBIT_HOST")
rabbit_port = os.environ.get("RABBIT_PORT")
rabbit_username = os.environ.get("RABBIT_USERNAME")
rabbit_password = os.environ.get("RABBIT_PASSWORD")
rabbit_queue = os.environ.get("RABBIT_QUEUE", "hello")

MESSAGES = []


def callback(ch, method, properties, body):
    print(" [x] Messages so far:")
    MESSAGES.append(body)
    print([json.loads(msg) for msg in MESSAGES])
    print(f"Messages: {len(MESSAGES)}")

    time.sleep(body.count(b"."))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def create_app():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
    channel = connection.channel()

    channel.queue_declare(queue=rabbit_queue, durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=rabbit_queue, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
