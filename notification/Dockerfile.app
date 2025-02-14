FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update && apt install -y curl &&\
    pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python utils/wait_for_pg.py &&\
                  python utils/wait_for_rabbitmq.py &&\
                  alembic upgrade heads &&\
                  gunicorn app.main:app \
                  --workers 4 \
                  --worker-class uvicorn.workers.UvicornWorker \
                  --bind 0.0.0.0:8000"]
