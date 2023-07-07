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

for i in range(10):
    start_time = datetime.now()
    cur.execute(
        f"SELECT * FROM views WHERE user_id = '{str(user_ids[0])}'"
        "AND movie_id = '{str(movie_ids[0])}'"
    )
    rows = cur.fetchall()
    print(datetime.now() - start_time)
