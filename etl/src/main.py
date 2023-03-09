"""
Statable ETL application for the online cinema project.
Performs the following process with base modules:
state -> psql, extractors -> transformers -> elastic
"""

from time import sleep

from etl_manager import EtlManager
from psql import PSQLManager
from settings import settings
from utils import backoff_decorator, psycopg2_conn_context


@backoff_decorator
def main():

    with psycopg2_conn_context(settings.PSQL_DSN) as conn:

        psql_manager = PSQLManager(conn)
        etl_manager = EtlManager(psql_manager)

        while True:

            etl_manager.start_filmwork_etl_process()
            etl_manager.start_genre_etl_process()
            etl_manager.start_person_etl_process()

            sleep(settings.SLEEP_DURATION)


if __name__ == '__main__':
    main()
