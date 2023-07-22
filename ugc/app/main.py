import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from app.api.v1 import views, bookmarks, reviews, movies
from app.core.config import config, kafka_config, mongo_config
from app.core.logger import LOGGING  # noqa
from app.db import redis, kafka, mongo
from app.core.jwt import configure_jwt
from app.errors import register_error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka.kafka_producer = AIOKafkaProducer(
        bootstrap_servers=f'{kafka_config.host}:{kafka_config.port}'
    )
    await kafka.kafka_producer.start()
    mongo.mongo_client = AsyncIOMotorClient(
        mongo_config.uri, server_api=ServerApi('1')
    )
    redis.redis = Redis(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db
    )

    yield

    await kafka.kafka_producer.stop()
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

app.include_router(views.router, prefix='/api/v1/views', tags=['views'])
app.include_router(movies.router, prefix='/api/v1/movies', tags=['movies'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
