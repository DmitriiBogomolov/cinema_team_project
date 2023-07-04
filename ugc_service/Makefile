all: kafka_deploy clickhouse_deploy create_topic create_shards etl

kafka_deploy:
	docker-compose -f kafka_service/docker-compose.yml up -d

clickhouse_deploy:
	docker-compose -f clickhouse_service/docker-compose.yml up -d

create_shards:
	# shard_1
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE DATABASE shard;"
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE DATABASE replica;"
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE TABLE shard.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/1/user_active', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);"
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE TABLE replica.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/2/user_active', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);"
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE TABLE events.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) ENGINE = Distributed('company_cluster', '', views, rand());"

	# shard_2
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE DATABASE shard;"
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE DATABASE replica;"
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE TABLE shard.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/2/user_active', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);"
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE TABLE replica.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/1/user_active', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);"
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE TABLE events.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) ENGINE = Distributed('company_cluster', '', views, rand());"

create_topic:
	docker exec -it broker /bin/kafka-topics --bootstrap-server localhost:9092 --create --topic views --partitions 4 --replication-factor 1\

.PHONY: etl
etl:
	docker build -t etl etl/.
	docker run -d --rm --name etl --network kafka --env-file .env.example etl
	docker network connect clickhouse etl

test:
	docker-compose -f tests/docker-compose.yml up test

clean:
	docker stop etl
	docker-compose -f kafka_service/docker-compose.yml down -v
	docker-compose -f clickhouse_service/docker-compose.yml down -v

test_run: all test clean
	docker-compose -f tests/docker-compose.yml down -v
