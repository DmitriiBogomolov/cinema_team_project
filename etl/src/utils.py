from contextlib import contextmanager
from functools import wraps
from time import sleep

import psycopg2
from pydantic import PostgresDsn

from logger import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """Backoff decorator implementation"""
    def func_wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            time_sleep = start_sleep_time
            while True:

                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception(e)
                    logger.info('Restarting function from backoff decorator')

                    sleep(time_sleep)
                    time_sleep *= factor
                    if time_sleep > border_sleep_time:
                        time_sleep = 10

        return inner

    return func_wrapper


backoff_decorator = backoff()


@backoff_decorator
@contextmanager
def psycopg2_conn_context(dsn: PostgresDsn):
    conn = psycopg2.connect(dsn)
    try:
        logger.info("Creating psql connection")
        yield conn
    finally:
        logger.info("Closing psql connection")
        conn.close()
