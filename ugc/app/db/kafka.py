from aiokafka import AIOKafkaProducer

kafka_producer: AIOKafkaProducer | None = None


async def get_kafka_producer():
    return kafka_producer
