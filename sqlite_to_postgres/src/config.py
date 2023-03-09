import os
from collections import namedtuple

from dotenv import load_dotenv

from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

load_dotenv()


DATA_CHUNK = 20

SCHEMA_PATH = os.environ.get('SCHEMA_PATH')
SQLITE_DB_PATH = os.environ.get('SQLITE_PATH')
POSTGRESQL_DSN = {
    'dbname': os.environ.get('PSQL_NAME'),
    'user': os.environ.get('PSQL_USER'),
    'password': os.environ.get('PSQL_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5500),
    'options': '-c search_path=content',
}

table_to_execute = namedtuple("TableToExecute", "table_name schema_name dataclass sqlite_columns")

TABLES_INFO = [
    table_to_execute('film_work',        'content', FilmWork,       ('id', 'title', 'description', 'creation_date', 'rating', 'type')),
    table_to_execute('genre',            'content', Genre,          ('id', 'name', 'description')                                    ),
    table_to_execute('genre_film_work',  'content', GenreFilmWork,  ('id', 'film_work_id', 'genre_id')                               ),
    table_to_execute('person',           'content', Person,         ('id', 'full_name')                                              ),
    table_to_execute('person_film_work', 'content', PersonFilmWork, ('id', 'film_work_id', 'person_id', 'role')                      )
]
