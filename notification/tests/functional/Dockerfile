FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ../ .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["sh", "-c", "python utils/wait_for_pg.py &&\
                  python utils/wait_for_rabbitmq.py &&\
                  pytest"]
