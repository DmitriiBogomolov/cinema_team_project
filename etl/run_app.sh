#!/usr/bin/env bash

chown www-data:www-data /var/log

rm -rf security
mkdir security

cp /usr/share/elasticsearch/config/certs/ca/ca.crt security/http_ca.crt

cd src

python main.py

