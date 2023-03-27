import os
import time

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es_host = f'{os.getenv("ELASTIC_HOST")}:{os.getenv("ELASTIC_PORT")}'
    es_client = Elasticsearch(hosts=es_host, validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
