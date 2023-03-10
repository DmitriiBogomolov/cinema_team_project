"""
Provides a object to garantee application state persistence
to continue running after the program stops.
    - state
"""

import abc
import json
import os
from json.decoder import JSONDecodeError
from typing import Optional

from redis import Redis

from logger import logger
from settings import settings
from utils import backoff_decorator


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, value: str, key: str) -> None:
        """Save state to the permanent storage"""
        pass

    @abc.abstractmethod
    def retrieve_state(self, key: str) -> str:
        """Load state from the permanent storage"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, value: str, key: str) -> None:
        mode = 'r+' if os.path.isfile(self.file_path) else 'a+'

        with open(self.file_path, mode) as write_file:
            try:
                d = json.load(write_file)
            except JSONDecodeError:
                d = {}

            d[key] = value
            write_file.seek(0)
            json.dump(d, write_file, indent=4)
            write_file.truncate()

    def retrieve_state(self, key: str) -> str:
        try:
            with open(self.file_path, "r") as read_file:
                d = json.load(read_file)
                return d.get(key)
        except (JSONDecodeError, FileNotFoundError):
            return None


class RedisStorage(BaseStorage):
    def __init__(self, redis_host: str):
        self.redis_adapter = Redis(settings.REDIS_HOST)

    @backoff_decorator
    def save_state(self, value: str, key: str) -> None:
        self.redis_adapter.set(key, value.encode())

    @backoff_decorator
    def retrieve_state(self, key: str) -> str:
        value = self.redis_adapter.get(key)
        return value.decode() if value else None


class State:
    """
    The class provides application state persistence
    to continue running after the program stops.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: str) -> None:
        """Set the state to a specific key"""
        self.storage.save_state(value, key)

    def get_state(self, key: str) -> str:
        """Get the state from a specific key"""
        return self.storage.retrieve_state(key)


class FakeState:
    """Development tool"""
    def set_state(self, key: str, value: str) -> None:
        pass

    def get_state(self, key: str) -> str:
        return '1000-10-10'


match settings.STATE_TYPE:
    case 'REDIS':
        logger.info('The programm was started in REDIS statable mode.')
        state = State(RedisStorage(settings.REDIS_HOST))

    case 'JSON':
        logger.info('The programm was started in JSON statable mode.')
        state = State(JsonFileStorage(settings.STATE_FILE_PATH))

    case 'FAKE':
        logger.info('The programm was started without state handling.')
        state = FakeState()
