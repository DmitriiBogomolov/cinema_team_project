"""
Statable ETL application for the online cinema project.
Performs the following process with base modules:
state -> psql, extractors -> transformers -> elastic
"""

from time import sleep

from elastic import ElasticManager
from etl_manager import EtlManager
from psql import PSQLManager
from settings import settings
from utils import backoff_decorator, psycopg2_conn_context


@backoff_decorator
def main():

    with psycopg2_conn_context(settings.PSQL_DSN) as conn:

        psql_manager = PSQLManager(conn)
        elastic_manager = ElasticManager()

        etl_manager = EtlManager(psql_manager, elastic_manager)
        etl_manager.create_schemas()

        while True:
            etl_manager.run()
            sleep(settings.SLEEP_DURATION)


if __name__ == '__main__':
    main()
