from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env.example'
        env_file_encoding = 'utf-8'


class KafkaSettings(Base):
    host: str = 'localhost'
    port: int = 9092
    topic_name: list = ['views']
    auto_offset_reset: str = 'earliest'
    group_id: str = 'clickhouse'
    enable_auto_commit: bool = False
    batch: int = 10000

    class Config:
        env_prefix = 'kafka_'

    @property
    def params(self):
        return {
            'bootstrap_servers': '{}:{}'.format(self.host, self.port),
            'auto_offset_reset': self.auto_offset_reset,
            'group_id': self.group_id,
            'enable_auto_commit': self.enable_auto_commit
        }


class ClickhouseSettings(Base):
    host: str = 'localhost'
    port: int = 9000
    user: str = 'admin'
    password: str = 123

    class Config:
        env_prefix = 'clickhouse_'


kafka_settings = KafkaSettings()
clickhouse_settings = ClickhouseSettings()
