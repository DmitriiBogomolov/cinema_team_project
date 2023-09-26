import uvicorn
import aio_pika
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from contextlib import asynccontextmanager
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.v1 import event_handler
from app.core.config import config, mongo_config, rabbit_config
from app.db import redis, mongo, rabbit
from app.core.jwt import configure_jwt
from app.errors import register_error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo.mongo_client = AsyncIOMotorClient(
        mongo_config.uri, server_api=ServerApi('1')
    )

    redis.redis = Redis(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db
    )

    #conn = await aio_pika.connect(rabbit_config.uri)
    #channel = await conn.channel()
    #rabbit.rabbit_producer_exchange = await channel.declare_exchange('message', type='direct', auto_delete=True)
    #queue_email = await channel.declare_queue('email', arguments={'x-max-priority': 10, 'x-message-ttl': 1800000})
    #await queue_email.bind(rabbit.rabbit_producer_exchange, 'email')

    yield

    await redis.redis.close()


app = FastAPI(
    title=config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


configure_jwt(app)
register_error_handlers(app)


app.include_router(event_handler.router, prefix='/api/v1/events', tags=['events'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
