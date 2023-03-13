FROM python:3.10-slim

WORKDIR /app

COPY requirements/common.txt requirements.txt

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]
