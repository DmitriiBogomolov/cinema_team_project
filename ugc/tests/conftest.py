import pytest
from kafka import KafkaProducer
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from tests.functional.fixtures.mongo import mongo_fixture

from tests.config import kafka_config, mongo_config


@pytest.fixture(scope='session')
def mongo_client():
    mongo_client = MongoClient(
        mongo_config.uri, server_api=ServerApi('1')
    )
    yield mongo_client


@pytest.fixture(scope='session')
def kafka_producer():
    session = KafkaProducer(bootstrap_servers=f'{kafka_config.host}:{kafka_config.port}')
    yield session


@pytest.fixture(scope='function')
def mongo_fixtures(mongo_client):
    mongo_client['ugc_db']['reviews'].insert_many(mongo_fixture['reviews'])


@pytest.fixture(autouse=True)
def clean_mongo(mongo_client):
    mongo_client['ugc_db']['bookmarks'].delete_many({})
    mongo_client['ugc_db']['filmworks_likes'].delete_many({})
    mongo_client['ugc_db']['reviews'].delete_many({})
    mongo_client['ugc_db']['reviews_likes'].delete_many({})
