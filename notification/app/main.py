import uvicorn
import aio_pika
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from contextlib import asynccontextmanager
from sqladmin import Admin

from app.api.v1 import events
from app.core.config import config, rabbit_config
from app.db import redis, rabbit, postgres
from app.core.jwt import configure_jwt
from app.errors import register_error_handlers
from app.views.views import StoredEventView, EmailTemlateView


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db
    )

    conn = await aio_pika.connect(rabbit_config.uri)
    channel = await conn.channel()
    rabbit.rabbit_producer_exchange = await channel.declare_exchange('message', type='direct', auto_delete=True)
    queue_email = await channel.declare_queue('email', arguments={'x-max-priority': 10, 'x-message-ttl': 1800000})
    await queue_email.bind(rabbit.rabbit_producer_exchange, 'email')

    await postgres.create_tables()

    yield

    await redis.redis.close()


app = FastAPI(
    title=config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

admin = Admin(app, postgres.engine)
admin.add_model_view(StoredEventView)
admin.add_model_view(EmailTemlateView)


configure_jwt(app)
register_error_handlers(app)


app.include_router(events.router, prefix='/api/v1/events', tags=['events'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
