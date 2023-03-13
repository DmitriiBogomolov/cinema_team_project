#!/usr/bin/env bash

cat .env-sample > .env

cd /app/src

python main.py
