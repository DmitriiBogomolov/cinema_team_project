from kafka import KafkaProducer
import uuid
from random import randint
from datetime import datetime
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092')

time_start = datetime.now()
for _ in range(1000000):
    user_id = uuid.uuid4()
    movie_id = uuid.uuid4()

    duration = randint(10, 7200)
    lenght_movie = randint(3600, 7200)
    event_time = int(datetime.timestamp(datetime.now()))

    producer.send(
        topic='views',
        key=bytes(f'{user_id},{movie_id}', encoding='utf-8'),
        value=bytes(json.dumps({'user_id': str(user_id),
                                'movie_id': str(movie_id),
                                'duration': duration,
                                'lenght_movie': lenght_movie,
                                'event_time': event_time}), encoding='utf-8')
    )

time_end = datetime.now()
print(time_end - time_start)
