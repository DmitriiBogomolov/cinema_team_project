import json
import os
from collections import namedtuple

from elasticsearch import Elasticsearch

Index = namedtuple('Index', ['index_name', 'schema_src'])


dirname = os.path.dirname(__file__)


indexes = [
    Index('movies', os.path.join(dirname, 'es_schemas/filmworks_schema.json')),
    Index('genres', os.path.join(dirname, 'es_schemas/genres_schema.json')),
    Index('persons', os.path.join(dirname, 'es_schemas/persons_schema.json')),
]


async def create_schema(es_client: Elasticsearch, index: Index) -> None:

    await es_client.indices.delete(index=index.index_name, ignore=[400, 404])

    with open(index.schema_src) as schema_file:
        index_schema = json.load(schema_file)
        await es_client.indices.create(
            index=index.index_name,
            settings=index_schema['settings'],
            mappings=index_schema['mappings'],
        )


async def create_schemas(es_client: Elasticsearch) -> None:
    for index in indexes:
        await create_schema(es_client, index)
