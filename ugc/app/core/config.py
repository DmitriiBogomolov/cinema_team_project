from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env.example'
        env_file_encoding = 'utf-8'


class AppConfig(Base):
    project_name: str = 'ugc_service'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0

    authjwt_secret_key: str

    dsn: str


class KafkaConfig(Base):
    host: str = 'broker'
    port: int = 9092
    topic_name: list = ['views']
    auto_offset_reset: str = 'earliest'
    group_id: str = 'clickhouse'
    batch: int = 10000

    class Config:
        env_prefix = 'kafka_'

    @property
    def params(self):
        return {
            'bootstrap_servers': '{}:{}'.format(self.host, self.port),
            'auto_offset_reset': self.auto_offset_reset,
            'group_id': self.group_id
        }


class MongoConfig(Base):
    uri: str

    class Config:
        env_prefix = 'mongo_'


config = AppConfig()
kafka_config = KafkaConfig()
mongo_config = MongoConfig()
