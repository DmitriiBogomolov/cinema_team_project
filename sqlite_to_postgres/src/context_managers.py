import sqlite3
from contextlib import contextmanager

from logger_config import logger

import psycopg2


@contextmanager
def sqlite3_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        logger.info("Creating sqlite connection")
        yield conn
    finally:
        logger.info("Closing sqlite connection")
        conn.close()


@contextmanager
def psycopg2_conn_context(dsn):
    conn = psycopg2.connect(**dsn)
    try:
        logger.info("Creating psql connection")
        yield conn
    finally:
        logger.info("Closing psql connection")
        conn.close()
