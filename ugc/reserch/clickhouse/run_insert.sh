#!/bin/bash

for ((i=1; i<11; i++))
do
sudo time -p -a -o time.txt docker exec -i clickhouse-node1 clickhouse-client --format_csv_delimiter=";" --query="INSERT INTO events.views FORMAT CSV" < data.csv
done
grep real time.txt
