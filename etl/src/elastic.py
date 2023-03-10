"""
Provides elsatic_manager with an active connection
(Elasticsearch client) to making queries.
Backoff after disconnect.
    - elsatic_manager
"""

import json
from collections.abc import Iterable

from elastic_transport import ConnectionError
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from logger import logger
from settings import settings
from utils import backoff_decorator


@backoff_decorator
def get_elastic_client() -> Elasticsearch:
    """
    Connect and returns Elasticsearch client object.
            Returns:
                es: Elasticsearch client object
    """

    es = Elasticsearch(settings.ELASTIC_HOST)
    return es


class ElasticManager:
    """
    Basic class for manage connection, making queries.

    Methods
    -------
    connect:
        create or update Elasticsearch client object

    bulk:
        bulk document collection

    create_filmwork_schema:
        сreate filmwork schema if not exist
    """

    def __init__(self):
        self.client = get_elastic_client()

    def connect(self) -> Elasticsearch:
        """Create or update Elasticsearch client object"""

        logger.info('Connect to Elasticsearch')
        self.client = get_elastic_client()
        return self.client

    def bulk(self, document_set: Iterable[dict]) -> None:
        """
        Bulk document collection.
            Parameters:
                document_set: сollection of prepared documents
        """
        while True:
            try:
                bulk(self.client, document_set)
                break
            except ConnectionError as e:
                logger.exception(e)
                self.connect()

    def create_filmwork_schema(self) -> None:
        """
        Create filmwork schema if not exist.
        """
        try:
            index_name = settings.INDEX_NAME
            if not self.client.indices.exists(index=index_name):
                logger.info('Creating elasticsearch schema.')
                with open(settings.SCHEMA_SRC) as schema_file:
                    index_schema = json.load(schema_file)
                self.client.indices.create(index=index_name, body=index_schema)
        except ConnectionError as e:
            logger.exception(e)
            self.connect()
        except FileNotFoundError as e:
            logger.exception(e)
            logger.error('Try to set SCHEMA_SRC in .env')


elsatic_manager = ElasticManager()
elsatic_manager.create_filmwork_schema()
