FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements/common.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["sh", "-c", "python utils/wait_for_pg.py & \
                  python utils/wait_for_redis.py & \
                  flask db upgrade & \
                  gunicorn -k gevent --bind=0.0.0.0:8002 'run:create_app()'"]
