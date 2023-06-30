import json
from clickhouse_driver import Client
from kafka import KafkaConsumer
from models import TableViews
from config import kafka_settings, clickhouse_settings


client = Client(**clickhouse_settings.dict())
consumer = KafkaConsumer(
    *kafka_settings.topic_name,
    **kafka_settings.params

)
query = 'INSERT INTO events.views FORMAT JSONEachRow'


def etl_process(client: Client, consumer: KafkaConsumer, query: str):
    values_string = []

    for message in consumer:
        row_view = TableViews(**json.loads(message.value))
        values_string.append(row_view.dict())
        if len(values_string) == 100000:
            client.execute(query, values_string)
            consumer.commit()
            values_string = []


if __name__ == '__main__':
    etl_process(client, consumer, query)
