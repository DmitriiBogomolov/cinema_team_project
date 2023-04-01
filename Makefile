.PHONY: start-etl start-api stop-api

CONTAINER_NAME = filmworks_api
ETL_NETWORK = etl_default

start-etl:
	cat etl/.env.example > etl/.env
	docker-compose -f "etl/docker-compose.yml" up -d

start-api:
	cat filmworks_api/.env-sample > filmworks_api/.env
	docker build -t $(CONTAINER_NAME):latest $(CONTAINER_NAME) \
	&& docker run -d --name $(CONTAINER_NAME) --network $(ETL_NETWORK) -p 8000:8000 $(CONTAINER_NAME):latest

stop-api:
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

start-service:
	cat etl/.env.example > etl/.env
	cat filmworks_api/.env-sample > filmworks_api/.env
	docker-compose up -d

run-tests:
	cat etl/.env.example > etl/.env
	cat filmworks_api/.env-sample > filmworks_api/.env
	cat filmworks_api/tests/functional/.env-sample > filmworks_api/tests/functional/.env
	docker-compose --project-name api_tests -f docker-compose.yaml -f docker-compose.tests.yaml up -d --build
