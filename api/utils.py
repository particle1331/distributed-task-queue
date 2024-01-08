import ast
import os

import pika

from dtq.app import app as celery_app


def exist_workers():
    inspector = celery_app.control.inspect()
    return inspector.ping() is not None


def poll_messages(queue="celery"):
    parameters = pika.ConnectionParameters(
        host=os.environ["RABBITMQ_HOST"],
        port=os.environ["RABBITMQ_PORT"],
    )
    conn = pika.BlockingConnection(parameters)
    queue_args = {"x-max-priority": 10}
    channel = conn.channel()
    channel.queue_declare(queue, durable=True, arguments=queue_args)

    messages = []
    while True:
        response = channel.basic_get(queue=queue, auto_ack=False)
        method_frame, properties, _ = response
        if method_frame is None:
            break

        metadata = properties.headers
        fields = [
            "id",
            "task",
            "retries",
            "timelimit",
            "root_id",
            "parent_id",
            "origin",
        ]
        msg = {metadata[k] for k in fields}
        msg["args"] = ast.literal_eval(metadata["argsrepr"])
        msg["kwargs"] = ast.literal_eval(metadata["kwargsrepr"])
        messages.append(msg)

    conn.close()
    return messages
