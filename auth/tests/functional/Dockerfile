FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements/dev.txt

EXPOSE 8000

CMD ["sh", "-c", "python utils/wait_for_pg.py & \
                  python utils/wait_for_redis.py & \
                  flask db upgrade & \
                  pytest"]
