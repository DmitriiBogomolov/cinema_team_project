.PHONY: start-etl start-api stop-api

CONTAINER_NAME = filmworks_api
ETL_NETWORK = etl_default

start-etl:
	docker-compose up --file etl/docker-compose.yml

start-api:
	docker build -t $(CONTAINER_NAME):latest $(CONTAINER_NAME) \
	&& docker run --name $(CONTAINER_NAME) --network $(ETL_NETWORK) -p 8000:8000 $(CONTAINER_NAME):latest

stop-api:
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

start-service: start-etl start-api
