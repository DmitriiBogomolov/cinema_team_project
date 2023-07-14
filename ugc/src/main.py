import uvicorn
import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_request_id import RequestContextMiddleware
from redis.asyncio import Redis
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager

from src.api.v1 import views
from src.core.config import config, kafka_config
from src.core.logger import LOGGING  # noqa
from src.db import redis
from src.db import kafka
from src.core.jwt import configure_jwt


sentry_sdk.init(
    dsn="https://638c9aa0fcb0458aaaf260317f41fe6a@o4505504683655168.ingest.sentry.io/4505505602076672",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka.kafka_producer = AIOKafkaProducer(
        bootstrap_servers=f'{kafka_config.host}:{kafka_config.port}'
    )
    await kafka.kafka_producer.start()
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
app.add_middleware(RequestContextMiddleware)
app.include_router(views.router, prefix='/api/v1/views', tags=['views'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=5000,
    )
