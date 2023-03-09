import sqlite3
from contextlib import contextmanager

import psycopg2


@contextmanager
def sqlite3_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    try:
        yield conn.cursor()
    finally:
        conn.close()


@contextmanager
def psycopg2_conn_context(dsn):
    conn = psycopg2.connect(**dsn)
    try:
        yield conn.cursor()
    finally:
        conn.close()
