FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements/common.txt requirements.txt

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt && python utils/wait_for_pg.py && python utils/wait_for_redis.py

EXPOSE 5000

CMD [ "python", "pywsgi.py" ]
