import csv
from datetime import datetime
from clickhouse_driver import Client
from config import clickhouse_settings


client = Client(**clickhouse_settings.dict())
query = """
    SELECT * FROM events.views
    WHERE user_id = %(user_id)s
    and movie_id = %(movie_id)s"""

with open('test_insert.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        data = {'user_id': row[0], 'movie_id': row[1]}
        start = datetime.now()
        client.execute(query, data)
        stop = datetime.now()
        print(stop - start)
