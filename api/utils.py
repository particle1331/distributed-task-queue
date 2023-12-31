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
    channel = conn.channel()
    channel.queue_declare(
        queue=queue, durable=True, arguments={"x-max-priority": 10}
    )

    messages = []
    while True:
        #  pylint: disable = unused-variable
        method_frame, properties, body = channel.basic_get(
            queue=queue,
            auto_ack=False,
        )
        if method_frame is None:
            break

        metadata = properties.headers
        metadata["task"] = metadata.pop("task")
        metadata["task_id"] = metadata.pop("id")
        metadata["args"] = ast.literal_eval(metadata.pop("argsrepr"))
        metadata["kwargs"] = ast.literal_eval(metadata.pop("kwargsrepr"))
        messages.append(metadata)

    conn.close()
    return messages
