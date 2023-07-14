import uvicorn
import sentry_sdk
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from fastapi_request_id import RequestContextMiddleware

from src.api.v1 import films, genres, persons
from src.core import cache
from src.core.config import cache_config, config
from src.db import elastic, redis
from src.core.jwt import configure_jwt


sentry_sdk.init(
    dsn="https://638c9aa0fcb0458aaaf260317f41fe6a@o4505504683655168.ingest.sentry.io/4505505602076672",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


app = FastAPI(
    title=config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=config.redis_host, port=config.redis_port, db=config.redis_db)
    elastic.es = AsyncElasticsearch(hosts=[f'{config.elastic_host}:{config.elastic_port}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.add_middleware(RequestContextMiddleware)
if cache_config.use_caching:
    app.middleware('http')(cache.cache_middleware)

configure_jwt(app)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
