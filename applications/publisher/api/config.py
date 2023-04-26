import os

rabbit_host = os.environ.get("RABBIT_HOST")
rabbit_port = os.environ.get("RABBIT_PORT")
rabbit_username = os.environ.get("RABBIT_USERNAME")
rabbit_password = os.environ.get("RABBIT_PASSWORD")
rabbit_queue = os.environ.get("RABBIT_QUEUE", "hello")
