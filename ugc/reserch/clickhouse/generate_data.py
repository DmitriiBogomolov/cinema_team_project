import uuid
import csv
from typing import Iterable
import os
from datetime import datetime
from random import randint


def generate_test_data(data_size: int) -> Iterable:

    for i in range(1, data_size + 1):

        user_id = uuid.uuid4()
        movie_id = uuid.uuid4()

        duration = randint(10, 7200)
        lenght_movie = randint(3600, 7200)
        event_time = int(datetime.timestamp(datetime.now()))

        with open('data.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([user_id, movie_id, duration, lenght_movie, event_time])

        if i % 3000000 == 0:
            with open('data_for_select.csv', 'a') as csvfile:
                writer_test_data = csv.writer(csvfile, delimiter=';')
                writer_test_data.writerow([user_id, movie_id])


if os.path.exists('data_for_select.csv'):
    os.remove('data_for_select.csv')
if os.path.exists('data.csv'):
    os.remove('data.csv')
generate_test_data(30000000)
