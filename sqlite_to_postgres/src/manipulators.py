import sqlite3
from dataclasses import astuple
from typing import List

from logger_config import logger
from models import IsDataclass
from config import SCHEMA_PATH

import psycopg2


def get_data_from_sqlite(sqlite_cursor: sqlite3.Connection.cursor, table_name: str,
                         columns: List[str], data_class: IsDataclass, data_chunk: int) -> list[IsDataclass]:
    columns_str = ', '.join(columns)

    try:
        sqlite_cursor.execute(f'SELECT {columns_str} FROM {table_name};')
    except sqlite3.OperationalError as e:
        logger.exception(e)
        return []

    while True:
        data = sqlite_cursor.fetchmany(data_chunk)
        data = [data_class(**dict(record)) for record in data]

        if data:
            yield data
        else:
            break


def load_data_to_postgresql(psycopg2_cursor: psycopg2.extensions.cursor,
                            table_name: str,
                            table_data: list[IsDataclass]) -> None:
    data_class_fields = table_data[0].__dataclass_fields__.keys()
    columns_str = ', '.join(data_class_fields)

    table_data = [astuple(instance) for instance in table_data]

    escaping_str = ', '.join(['%s'] * len(data_class_fields))
    args = ','.join(psycopg2_cursor.mogrify(f'({escaping_str})', item).decode() for item in table_data)

    try:
        psycopg2_cursor.execute(f'''
        INSERT INTO {table_name} ({columns_str})
        VALUES {args}
        ''')
    except psycopg2.OperationalError as e:
        logger.exception(e)


def truncate_psql_table(psycopg2_cursor: psycopg2.extensions.cursor, table_name):
    try:
        psycopg2_cursor.execute(f'''TRUNCATE {table_name} CASCADE''')
    except psycopg2.OperationalError as e:
        logger.exception(e)


def create_schema(psycopg2_cursor: psycopg2.extensions.cursor):
    psycopg2_cursor.execute(open(SCHEMA_PATH, 'r').read())
