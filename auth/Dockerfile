FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update && apt install -y curl &&\
    pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python utils/wait_for_pg.py & \
                  python utils/wait_for_redis.py & \
                  flask db upgrade & \
                  flask load_debug_data & \
                  gunicorn -k gevent --bind=0.0.0.0:8000 'run:create_app()'"]
