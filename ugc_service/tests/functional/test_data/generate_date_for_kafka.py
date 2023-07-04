import uuid
import json
from typing import Iterable
from datetime import datetime
from random import randint


def generate_test_data(count_data: int) -> Iterable:
    for _ in range(count_data):
        user_id = uuid.uuid4()
        movie_id = uuid.uuid4()

        duration = randint(10, 7200)
        lenght_movie = randint(3600, 7200)
        event_time = int(datetime.timestamp(datetime.now()))

        key = bytes(f'{user_id},{movie_id}', encoding='utf-8')
        data = bytes(json.dumps({'user_id': str(user_id),
                                 'movie_id': str(movie_id),
                                 'duration': duration,
                                 'lenght_movie': lenght_movie,
                                 'event_time': event_time}), encoding='utf-8')
        yield key, data
