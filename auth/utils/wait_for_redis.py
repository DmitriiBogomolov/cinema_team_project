import os
import sys
import time

from redis import Redis

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from app.core.config import config
from app.core.logger import logger

if __name__ == '__main__':
    redis_client = Redis(
        host=config.redis_host,
        port=config.redis_port
    )
    while True:
        if redis_client.ping():
            logger.info('Database redis is available.')
            break
        time.sleep(1)
