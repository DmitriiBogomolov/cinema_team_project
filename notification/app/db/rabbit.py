from aio_pika import Exchange


rabbit_producer_exchange: Exchange | None = None


async def get_rabbit_producer():
    return rabbit_producer_exchange
