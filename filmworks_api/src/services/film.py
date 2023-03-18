from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Filmwork

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Filmwork]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Filmwork]:
        """Возвращает полную информацию о фильме из эластика по id"""
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        data = doc['_source']
        return Filmwork(
            id=data['id'],
            title=data['title'],
            imdb_rating=data['imdb_rating'],
            description=data['description'],
            genres=data['genres'],
            actors=data['actors'],
            writers=data['writers'],
            directors=data['directors'],
            )

    async def get_search_list(self, params) -> Optional[Filmwork]:
        """Возвращает список фильмов"""
        films = await self._get_search_from_elastic(*params)
        if not films:
            return None
        return films

    async def _get_search_from_elastic(
            self,
            query: str,
            page_size: int,
            page_number: int,
            ) -> Optional[Filmwork]:
        try:
            search = {
                'from': page_size * (page_number-1),
                'size': page_size,
                'query': {
                    'multi_match': {
                        'query': query,
                        'fuzziness': 'auto',
                        'fields': [
                            'title',
                            'description',
                            'genres_names',
                            'actors_names',
                            'writers_names',
                            'directors_names'
                        ]
                    }
                }
            }
            res = await self.elastic.search(index='movies', doc_type='_doc', body=search)
        except NotFoundError:
            return None
        movies = []
        for doc in res['hits']['hits']:
            movies.append(Filmwork(**doc['_source']))
        return movies

    async def get_list(self, params) -> Optional[Filmwork]:
        """Возвращает список фильмов"""
        films = await self._get_films_from_elastic(*params)
        if not films:
            return None
        return films

    async def _get_films_from_elastic(
            self,
            genre_id: str,
            sort: str,
            page_size: int,
            page_number: int,
            ) -> Optional[Filmwork]:
        try:
            # если параметры пагинации не указаны,
            # по умолчанию будет выведено 50 записей на первой странице
            search = {
                'from': page_size * (page_number-1),  # колво пропущенных записей
                'size': page_size,
                'query': {
                    'match_all': {}
                }
            }
            # делаем запрос по жанрам
            if genre_id:
                search['query'] = {
                    'bool': {
                        'must': [
                            {'match': {'genres.id': genre_id}},
                        ]
                    }
                }
            # подключаем сортировку только по рейтингу
            if sort == '-imdb_rating':
                search['sort'] = [
                        {'imdb_rating': {'order': 'desc'}}
                    ]
            res = await self.elastic.search(index='movies', doc_type='_doc', body=search)
        except NotFoundError:
            return None
        movies = []
        for doc in res['hits']['hits']:
            movies.append(Filmwork(**doc['_source']))
        return movies

    async def _film_from_cache(self, film_id: str) -> Optional[Filmwork]:
        """Возвращает фильм из кеша по id"""
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Filmwork.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Filmwork):
        """Добавляем фильм в кеш"""
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
