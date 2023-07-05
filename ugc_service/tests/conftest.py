import pytest
from typing import Iterable
from clickhouse_driver import Client
from kafka import KafkaProducer

from tests.config import kafka_settings, clickhouse_settings


@pytest.fixture(scope='session')
def client_clickhouse():
    session = Client(**clickhouse_settings.dict())
    yield session


@pytest.fixture(scope='session')
def kafka_producer():
    session = KafkaProducer(bootstrap_servers=f'{kafka_settings.host}:{kafka_settings.port}')
    yield session


@pytest.fixture
def write_to_kafka(kafka_producer):
    def inner(data: Iterable, topic_name: str):
        for key, value in data:
            kafka_producer.send(topic=topic_name, key=key, value=value)
    return inner
