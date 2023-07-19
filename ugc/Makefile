run_all: deploy_kafka deploy_mongo deploy_clickhouse create_kafka_topics create_mongo_shards create_clickhouse_shards deploy_etl

run_service: deploy_kafka deploy_mongo create_kafka_topics create_mongo_shards

deploy_kafka:
	docker-compose -f kafka/docker-compose.yml up -d

create_kafka_topics:
	docker exec -it broker /bin/kafka-topics --bootstrap-server localhost:9092 --create --topic views --partitions 4 --replication-factor 1\

deploy_mongo:
	docker-compose -f mongo/docker-compose.yml up -d

create_mongo_shards:
	# Настраиваем серверы конфигурации MongoDB
	docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, ]})" | mongosh'

	# Собираем шарды MongoDB
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}]})" | mongosh'
	docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}]})" | mongosh'

	# Дожидаемся работоспособности шардов MongoDB
	sh mongo/whait_shards.sh mongors1n1
	sh mongo/whait_shards.sh mongors2n1

	# Подключаем шарды к маршрутизатору MongoDB
	docker exec -it mongos bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
	docker exec -it mongos bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'

	# Создаем базу данных и включаем шардирование MongoDB
	docker exec -it mongors1n1 bash -c 'echo "use ugc_db" | mongosh'
	docker exec -it mongos bash -c 'echo "sh.enableSharding(\"ugc_db\")" | mongosh'

	# Создаем коллекции MongoDB
	docker exec -it mongos bash -c 'echo "db.createCollection(\"ugc_db.filmworks_likes\")" | mongosh'
	docker exec -it mongos bash -c 'echo "db.createCollection(\"ugc_db.reviews_likes\")" | mongosh'
	docker exec -it mongos bash -c 'echo "db.createCollection(\"ugc_db.reviews\")" | mongosh'
	docker exec -it mongos bash -c 'echo "db.createCollection(\"ugc_db.bookmarks\")" | mongosh'

	# Включаем шардирование для коллекций MongoDB
	# с уникальным композитным ключом для filmworks_likes, reviews_likes, bookmarks
	docker exec -it mongos bash -c 'echo "sh.shardCollection(\"ugc_db.filmworks_likes\", {\"user_id\" : 1, \"entity_id\" : 1 }, { unique: true })" | mongosh'
	docker exec -it mongos bash -c 'echo "sh.shardCollection(\"ugc_db.reviews_likes\", {\"user_id\" : 1, \"entity_id\" : 1 }, { unique: true })" | mongosh'
	docker exec -it mongos bash -c 'echo "sh.shardCollection(\"ugc_db.reviews\", {\"_id\": \"hashed\"})" | mongosh'
	docker exec -it mongos bash -c 'echo "sh.shardCollection(\"ugc_db.bookmarks\", {\"user_id\" : 1, \"movie_id\" : 1 }, { unique: true })" | mongosh'

deploy_clickhouse:
	docker-compose -f clickhouse/docker-compose.yml up -d

create_clickhouse_shards:
	# Собираем первый шард ClickHouse
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE DATABASE shard;"
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE DATABASE replica;"
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE TABLE shard.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/1/user_active', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);"
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE TABLE replica.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/2/user_active', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);"
	docker exec -it clickhouse-node1 clickhouse-client --query="CREATE TABLE events.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) ENGINE = Distributed('company_cluster', '', views, rand());"

	# Собираем второй шард ClickHouse
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE DATABASE shard;"
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE DATABASE replica;"
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE TABLE shard.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/2/user_active', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);"
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE TABLE replica.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/1/user_active', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY (user_id, movie_id);"
	docker exec -it clickhouse-node3 clickhouse-client --query="CREATE TABLE events.views (user_id UUID, movie_id UUID, duration UInt32, lenght_movie UInt32, event_time DateTime) ENGINE = Distributed('company_cluster', '', views, rand());"

.PHONY: etl
deploy_etl:
	docker build -t etl etl/.
	docker run -d --rm --name etl --network kafka --env-file .env.example etl
	docker network connect clickhouse etl

test_etl:
	docker-compose -f etl/tests/docker-compose.yml up test

run_test_etl: run_all test_etl clean
	docker-compose -f etl/tests/docker-compose.yml down -v

clean:
	docker stop etl || true
	docker-compose -f kafka/docker-compose.yml down -v
	docker-compose -f mongo/docker-compose.yml down -v
	docker-compose -f clickhouse/docker-compose.yml down -v
