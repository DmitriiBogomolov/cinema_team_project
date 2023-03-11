"""
Provides psql_manager with an active psycopg2 connection
to making queries. Backoff after disconnect.
    - psql_manager
"""

from contextlib import closing
from typing import List

import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection
from psycopg2.extras import RealDictRow

from logger import logger
from settings import settings


class PSQLManager:
    """Basic class for manage psql connection, making queries."""

    def __init__(self, conn: connection):
        self.conn = conn

    def get_execution_generator(self, query_str: str) -> List[RealDictRow]:
        """
        Make query and returns generator.
            Parameters:
                query_str: query string
            Returns:
                data: fetched List[RealDictRow] with DATA_CHUNK len

        """

        logger.info('Making query from psql.')

        with closing(self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)) as cursor:

            cursor.execute(query_str)

            while True:
                data = list(cursor.fetchmany(settings.DATA_CHUNK))

                if data:
                    yield data
                else:
                    break
