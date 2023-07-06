# pylint: disable=unused-argument
import logging
import time

from celery.exceptions import WorkerShutdown
from celery.signals import task_failure, worker_init
from celery.utils.log import get_logger


@worker_init.connect
def setup_workers(sender=None, conf=None, **kwargs):
    logging.basicConfig(
        filename="worker_init.log",
        filemode="w",
        format="[%(asctime)s: %(levelname)s/%(name)s] %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger("WorkerInit")
    try:
        logger.info("Starting worker...")
        time.sleep(12.0)
        logger.info("Worker started successfully.")
    except Exception as exc:
        logger.error(exc, exc_info=True)
        logger.critical("Failed to start worker. Shutting down...")
        raise WorkerShutdown() from exc


@task_failure.connect
def task_failure_notifier(sender=None, task_id=None, **kwargs):
    logger = get_logger("celery")
    message = f"[task_failure_notifier]: Task {sender.name} failed successfully!"
    logger.error(message)
