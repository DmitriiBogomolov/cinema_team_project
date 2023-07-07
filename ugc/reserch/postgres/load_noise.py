import psycopg2

from tools import read_lines_in_batches

conn = psycopg2.connect(
    host='127.0.0.1',
    port=5500,
    dbname='movies_database',
    user='app',
    password='123qwe'
)
cur = conn.cursor()

cur.execute('TRUNCATE views CASCADE')


i = 1
for batch in read_lines_in_batches('noise.txt', 1000):
    values = [n.replace('\n', '').split(', ') for n in batch]
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
    print(i)
    i += 1

cur.execute('SELECT count(*) FROM views')
records = cur.fetchall()


print(records)
