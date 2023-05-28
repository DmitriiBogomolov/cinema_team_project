import os
import sys
import time

from redis import Redis

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from config import config


if __name__ == '__main__':
    redis_client = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT
    )
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
