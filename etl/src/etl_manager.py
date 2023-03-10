"""
Provides EtlManager wich startup ETL processes
    - EtlManager
"""

from elastic import elsatic_manager
from extractors import extract_query_statable
from logger import logger
from psql import PSQLManager
from psql_queries import (query_filmworks_by_genres_modified_date,
                          query_filmworks_by_modified_date,
                          query_filmworks_by_person_modified_date)
from transformers import prepare_filmwork_documents


class EtlManager():
    """
    Basic class for manage ETL processes.

    Methods
    -------
    start_base_etl_process: represents standart ETL flow
                    gets data -> preform data portion -> bulk it to elastic

    start_filmwork_etl_process: iterate over modified filmwork records
                                bulk filmwolk documents

    start_genre_etl_process: iterate over modified genre records
                                bulk filmwolk documents

    start_person_etl_process: iterate over modified person records
                                bulk filmwolk documents
    """

    def __init__(self, psql_manager: PSQLManager):
        self.psql_manager = psql_manager

    def start_base_etl_process(self, keyword: str, query_str: str):
        """
        Base ETL process handler.
        gets data -> preform data portion -> bulk it to elastic

                Parameters:
                    keyword: state keyword for ETL process
                    query_str: SQL query template

        """

        logger.info(f'Starts ETL process: {keyword}')

        data_generator = extract_query_statable(keyword, query_str, self.psql_manager)

        for data_set in data_generator:

            document_set = prepare_filmwork_documents(data_set)
            elsatic_manager.bulk(document_set)

    def start_filmwork_etl_process(self):
        keyword = 'filmwork_last_modified'
        query_str = query_filmworks_by_modified_date

        self.start_base_etl_process(keyword, query_str)

    def start_genre_etl_process(self):
        keyword = 'genre_last_modified'
        query_str = query_filmworks_by_genres_modified_date

        self.start_base_etl_process(keyword, query_str)

    def start_person_etl_process(self):
        keyword = 'person_last_modified'
        query_str = query_filmworks_by_person_modified_date

        self.start_base_etl_process(keyword, query_str)
