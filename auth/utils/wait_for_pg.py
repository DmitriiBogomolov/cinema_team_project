import os
import sys
import time

import psycopg2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from app.core.config import config
from app.core.logger import logger


def is_database_available():
    try:
        conn = psycopg2.connect(
            dbname=config.postgres_db,
            user=config.postgres_user,
            password=config.postgres_password,
            host=config.postgres_host,
            port=config.postgres_port,
        )
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        logger.warning(e)
        return False


def check_database_availability():
    timeout = 1
    while not is_database_available():
        logger.info('Waiting for the database to be available...')
        time.sleep(timeout)
        timeout += 1
    logger.info('Database postgres is available.')


if __name__ == '__main__':
    check_database_availability()
