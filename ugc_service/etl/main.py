import json
import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError
from kafka import KafkaConsumer
from models import TableViews
from logger import logger
from config import kafka_settings, clickhouse_settings


client = Client(**clickhouse_settings.dict())
consumer = KafkaConsumer(
    *kafka_settings.topic_name,
    **kafka_settings.params

)
query = 'INSERT INTO events.views FORMAT JSONEachRow'


@backoff.on_exception(backoff.expo, NetworkError)
def insert_clickhouse(client: Client, query: str, data: list):
    client.execute(query, data)


def etl_process(client: Client, consumer: KafkaConsumer, query: str):
    values_string = []

    for message in consumer:
        row_view = TableViews(**json.loads(message.value))
        values_string.append(row_view.dict())
        logger.info(len(values_string))

        if len(values_string) == kafka_settings.batch:
            logger.info(f'{kafka_settings.batch} rows loaded')
            insert_clickhouse(client, query, values_string)
            consumer.commit()
            values_string = []


if __name__ == '__main__':
    etl_process(client, consumer, query)
