from dataclasses import dataclass
from psycopg2.extensions import connection, cursor


@dataclass
class PSQL:
    conn: connection
    cursor: cursor
