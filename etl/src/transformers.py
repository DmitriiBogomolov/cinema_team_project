"""
Provides a function to transform:
raw data from extractor -> collection of documents for elastic
"""

from typing import List

from psycopg2.extras import RealDictRow

from models import Filmwork, Nested, Genre, Person


def prepare_filmwork_documents(raw_data_set: List[RealDictRow], index_name: str) -> List[dict]:
    """Transform a collection of raw_data from extractor to list of elastic documents"""

    documents = []

    for filmwork_raw in raw_data_set:

        directors, actors, writers = [], [], []
        for person in filmwork_raw['persons']:

            if person['person_role'] == 'DR':
                directors.append(Nested(id=person['person_id'], name=person['person_name']))
            elif person['person_role'] == 'AR':
                actors.append(Nested(id=person['person_id'], name=person['person_name']))
            elif person['person_role'] == 'WR':
                writers.append(Nested(id=person['person_id'], name=person['person_name']))

        filmwork = Filmwork(
            id=filmwork_raw['id'],
            imdb_rating=filmwork_raw['rating'],
            genre=filmwork_raw['genres'],
            title=filmwork_raw['title'],
            description=filmwork_raw['description'],
            directors=directors,
            actors=actors,
            writers=writers,
            directors_names=[d.name for d in directors],
            actors_names=[a.name for a in actors],
            writers_names=[w.name for w in writers],
        )

        documents.append({
            '_index': index_name,
            '_id': filmwork.id,
            '_source': filmwork.dict()
        })

    return documents


def prepare_genre_documents(raw_data_set: List[RealDictRow], index_name: str) -> List[dict]:
    """Transform a collection of raw_data from extractor to list of elastic documents"""

    documents = []

    for genre_raw in raw_data_set:

        genre = Genre(
            id=genre_raw['id'],
            name=genre_raw['name'],
            description=genre_raw['description'],
        )

        documents.append({
            '_index': index_name,
            '_id': genre.id,
            '_source': genre.dict()
        })

    return documents


def prepare_person_documents(raw_data_set: List[RealDictRow], index_name: str) -> List[dict]:
    """Transform a collection of raw_data from extractor to list of elastic documents"""

    documents = []

    for person_raw in raw_data_set:

        person = Person(
            id=person_raw['id'],
            full_name=person_raw['full_name']
        )
        documents.append({
            '_index': index_name,
            '_id': person.id,
            '_source': person.dict()
        })

    return documents
