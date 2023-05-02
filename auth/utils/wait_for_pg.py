import os
import sys
import time

import psycopg2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from settings import app_settings


def is_database_available():
    try:
        conn = psycopg2.connect(
            dbname=app_settings.PG_DB,
            user=app_settings.PG_USER,
            password=app_settings.PG_PASSWORD,
            host=app_settings.PG_HOST,
            port=app_settings.PG_PORT,
        )
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False


def check_database_availability():
    timeout = 1
    while not is_database_available():
        print('Waiting for the database to be available...')
        time.sleep(timeout)
        timeout += 1
    print('Database is available.')


if __name__ == '__main__':
    check_database_availability()
