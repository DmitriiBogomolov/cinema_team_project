import time

from redis import Redis

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
