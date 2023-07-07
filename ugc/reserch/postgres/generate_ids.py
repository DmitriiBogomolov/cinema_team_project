import uuid

user_ids = [str(uuid.uuid4()) for _ in range(10)]
movie_ids = [str(uuid.uuid4()) for _ in range(10)]


with open('ids.txt', 'w') as f:
    f.write(', '.join(user_ids) + '\n')
    f.write(', '.join(user_ids) + '\n')
