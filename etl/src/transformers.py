"""
Provides a function to transform:
raw data from extractor -> collection of documents for elastic
    - prepare_filmwork_documents
"""

from typing import List

from psycopg2.extras import RealDictRow

from models import Filmwork, Nested
from settings import settings


def filmwork_raw_to_object(filmwork_raw: RealDictRow) -> Filmwork:
    """Transform raw data object from extractor to model object"""

    directors, actors, writers = [], [], []
    for person in filmwork_raw['persons']:
        match person['person_role']:
            case 'DR':
                directors.append(Nested(id=person['person_id'], name=person['person_name']))
            case 'AR':
                actors.append(Nested(id=person['person_id'], name=person['person_name']))
            case 'WR':
                writers.append(Nested(id=person['person_id'], name=person['person_name']))

    filmwork = Filmwork(
        id=filmwork_raw['id'],
        imdb_rating=filmwork_raw['rating'],
        genre=filmwork_raw['genres'],
        title=filmwork_raw['title'],
        description=filmwork_raw['description'],
        director=[d.name for d in directors],
        actors=actors,
        writers=writers,
        actors_names=[a.name for a in actors],
        writers_names=[w.name for w in writers],
    )
    return filmwork


def filmwork_object_to_document(filmwork_object: Filmwork) -> dict:
    """Transform model object to elasticsearch document"""
    filmwork = filmwork_object.dict()
    id = filmwork['id']
    return {'_index': settings.INDEX_NAME, '_id': id, '_source': filmwork}


def prepare_filmwork_documents(raw_data_set: List[RealDictRow]) -> List[dict]:
    """Transform a collection of raw_data from extractor to list of elastic documents"""

    filmwork_objects = map(filmwork_raw_to_object, raw_data_set)
    documents = map(filmwork_object_to_document, filmwork_objects)

    return list(documents)
