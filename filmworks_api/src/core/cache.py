import json
from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse, Response

from src.db.redis import get_redis

CACHE_TTL = 60


async def cache_middleware(request: Request, call_next):
    redis_client = await get_redis()
    key = f'{request.method}:{request.url.path}'
    if request.query_params:
        key += f'?{request.query_params}'
    cached_response = await redis_client.get(key)
    if cached_response is not None:
        return JSONResponse(json.loads(cached_response.decode()))

    response = await call_next(request)

    if response.status_code == HTTPStatus.OK:
        response_body = b''
        async for chunk in response.body_iterator:
            response_body += chunk
        await redis_client.set(key, response_body.decode(), ex=CACHE_TTL)
        response = Response(content=response_body, status_code=response.status_code,
                            headers=dict(response.headers), media_type=response.media_type)

    return response
