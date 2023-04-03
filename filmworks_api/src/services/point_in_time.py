from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from src.core.config import pit_config
from src.db.elastic import get_elastic
from src.db.redis import get_redis


class PITService:
    """
    Generates elsaticsearch point in time token for a specific index.
    Returns a new token if the previous one has lifetime expired.
    https://www.elastic.co/guide/en/elasticsearch/reference/7.17/point-in-time-api.html
    """

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_pit_token(self, index_name: str) -> str:
        """If rotation enabled, tries to take it from redis."""

        if not pit_config.use_pit_rotation:
            return await self.get_new_pit_token(index_name)

        pit_key = f'{index_name}_PIT'
        pit_token = await self._get_from_redis(pit_key)

        if not pit_token:
            pit_token = await self.get_new_pit_token(index_name)

            await self._set_to_redis(pit_key, pit_token)

        return pit_token

    async def get_new_pit_token(self, index_name: str) -> str:
        """Generate a new token with `pit_max_age` lifetime (in seconds)."""

        keep_alive = f'{str(pit_config.pit_max_age + 20)}s'
        pit_token = await self.elastic.open_point_in_time(
                            index_name,
                            params={'keep_alive': keep_alive},
                            headers=None
                            )
        pit_token = pit_token['id']
        return pit_token

    async def _get_from_redis(self, pit_key: str) -> str | None:
        """Tries to take token from from redis"""

        pit_token = await self.redis.get(pit_key)
        if not pit_token:
            return None

        return pit_token.decode()

    async def _set_to_redis(self, pit_key: str, pit_token: str) -> None:
        """Save token for a `pit_max_age` seconds."""

        await self.redis.set(pit_key, pit_token, pit_config.pit_max_age)


@lru_cache()
def get_pit_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PITService:
    return PITService(redis, elastic)
