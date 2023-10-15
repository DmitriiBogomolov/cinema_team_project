import os
import sys
import time

import pika
from pika.exceptions import AMQPConnectionError

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from app.core.config import rabbit_config as config
from app.core.logger import logger


def is_rabbitmq_available():
    try:
        pika.BlockingConnection(
            pika.URLParameters(config.uri)
        )
        return True
    except AMQPConnectionError as e:
        logger.warning(e)
        return False


def check_rabbitmq_availability():
    timeout = 1
    while not is_rabbitmq_available():
        logger.info('Waiting for the rabbitmq to be available...')
        time.sleep(timeout)
        timeout += 1
    logger.info('Rabbitmq is available.')


if __name__ == '__main__':
    check_rabbitmq_availability()
