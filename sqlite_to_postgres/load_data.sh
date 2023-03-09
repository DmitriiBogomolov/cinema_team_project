#!/usr/bin/env bash

chown www-data:www-data /var/log

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done 

cd /opt/app/src

python main.py
