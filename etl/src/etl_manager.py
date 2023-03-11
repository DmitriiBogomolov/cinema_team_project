"""
Provides EtlManager wich startup ETL processes
    - EtlManager
"""

from typing import Callable

from pydantic import BaseModel

from elastic import ElasticManager
from extractors import extract_query_statable
from logger import logger
from psql import PSQLManager
from psql_queries import (query_filmworks_by_genres_modified_date,
                          query_filmworks_by_modified_date,
                          query_filmworks_by_person_modified_date,
                          query_genres_by_modified_date,
                          query_persons_by_modified_date
                          )
from settings import settings
from transformers import prepare_filmwork_documents, prepare_genre_documents, prepare_person_documents


class ETLSegment(BaseModel):
    """ETL process can contain a few segments."""
    keyword: str
    query_str: str
    transform_func: Callable
    index_name: str


ETL_PROCESSES = {
    'filmwork_etl_process': [
        ETLSegment(
            keyword='FILMWORK_ETL_filmwork_last_modified',
            query_str=query_filmworks_by_modified_date,
            transform_func=prepare_filmwork_documents,
            index_name='movies'
        ),
        ETLSegment(
            keyword='FILMWORK_ETL_genre_last_modified',
            query_str=query_filmworks_by_genres_modified_date,
            transform_func=prepare_filmwork_documents,
            index_name='movies'
        ),
        ETLSegment(
            keyword='FILMWORK_ETL_person_last_modified',
            query_str=query_filmworks_by_person_modified_date,
            transform_func=prepare_filmwork_documents,
            index_name='movies'
        ),
    ],
    'genre_etl_process': [
        ETLSegment(
            keyword='GENRE_ETL_last_modified',
            query_str=query_genres_by_modified_date,
            transform_func=prepare_genre_documents,
            index_name='genres'
        )
    ],
    'person_etl_process': [
        ETLSegment(
            keyword='PERSON_ETL_last_modified',
            query_str=query_persons_by_modified_date,
            transform_func=prepare_person_documents,
            index_name='persons'
        )
    ]
}


class EtlManager:
    """Basic class for manage ETL processes."""

    def __init__(self, psql_manager: PSQLManager, elastic_manager: ElasticManager):
        self.psql_manager = psql_manager
        self.elastic_manager = elastic_manager
        self.etl_processes = ETL_PROCESSES

    def base_segment_handler(self, etl_segment: ETLSegment):
        """
        Represents standart ETL flow
            gets data -> preform data portion -> bulk it to elastic
        """
        data_generator = extract_query_statable(
                etl_segment.keyword,
                etl_segment.query_str,
                self.psql_manager
        )

        for data_set in data_generator:

            document_set = etl_segment.transform_func(data_set, etl_segment.index_name)
            self.elastic_manager.bulk(document_set)

    def create_schemas(self):
        for index_name, schema_src in settings.SCHEMAS_DESTINATION:
            self.elastic_manager.create_schema(index_name, schema_src)

    def run(self):
        """Startup ETL PROCESSES"""
        for etl_name in self.etl_processes.keys():

            logger.info(f'Starts ETL process: {etl_name}')

            for etl_segment in self.etl_processes[etl_name]:
                """Each process can contain a few scenario."""
                self.base_segment_handler(etl_segment)
