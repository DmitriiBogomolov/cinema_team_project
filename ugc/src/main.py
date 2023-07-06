import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from src.api.v1 import views
from src.core.config import config
from src.core.logger import LOGGING  # noqa
from src.db import redis
from src.core.jwt import configure_jwt

app = FastAPI(
    title=config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=config.redis_host, port=config.redis_port, db=config.redis_db)


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()


configure_jwt(app)

app.include_router(views.router, prefix='/api/v1/views', tags=['views'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
