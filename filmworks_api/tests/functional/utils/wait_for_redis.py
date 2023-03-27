import os
import time

from redis import Redis

if __name__ == '__main__':
    redis_client = Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        db=os.getenv('REDIS_DB')
    )
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
