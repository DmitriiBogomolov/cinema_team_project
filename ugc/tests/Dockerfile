FROM python:3.11-alpine

WORKDIR /usr/src/tests

COPY requirements.txt .

RUN apk update && apk add --no-cache bash \
    && apk add --no-cache curl \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "pytest", "functional" ]
