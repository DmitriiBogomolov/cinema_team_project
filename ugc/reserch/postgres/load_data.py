import uuid
from datetime import datetime

import psycopg2


with open('ids.txt', 'r') as f:
    user_ids, movie_ids = [n.strip().split(', ') for n in f.readlines()]


conn = psycopg2.connect(
    host='127.0.0.1',
    port=5500,
    dbname='movies_database',
    user='app',
    password='123qwe'
)
cur = conn.cursor()

BATCH_SIZE = 333000

for i in range(10):

    start_time = datetime.now()

    values = [
        (str(uuid.uuid4()), user_ids[i], movie_ids[i], 100, 2000, '2023-07-07')
        for _ in range(BATCH_SIZE)
    ]
    cur.executemany("""
        INSERT INTO views
                    (id,
                    user_id,
                    movie_id,
                    duration,
                    lenght_movie,
                    event_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, values)
    conn.commit()

    print(datetime.now() - start_time)
