from diagrams import Diagram, Cluster
from diagrams.c4 import Container
from diagrams.onprem.database import ClickHouse
from diagrams.onprem.queue import Kafka


with Diagram('Sprint-8-elt-decomposition', show=False, direction='TB'):
    with Cluster('UGC ETL'):
        kafka_connector = Container(
            name='Kafka connector',
        )
        transformer = Container(
            name='Transformer',
        )
        clickhouse_connector = Container(
            name='ClickHouse connector',
        )
        kafka_connector >> transformer >> clickhouse_connector

    Kafka('Kafka') >> kafka_connector
    clickhouse_connector >> ClickHouse('ClickHouse')
