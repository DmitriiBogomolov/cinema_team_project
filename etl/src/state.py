"""
Provides a object to garantee application state persistence
to continue running after the program stops.
    - state
"""

import abc
import json
import os
from json.decoder import JSONDecodeError
from typing import Any, Optional

from logger import logger
from settings import settings


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, value: dict, key: str) -> None:
        """Save state to the permanent storage"""
        pass

    @abc.abstractmethod
    def retrieve_state(self, key: str) -> dict:
        """Load state from the permanent storage"""
        pass


class JsonFileStorage(BaseStorage):

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, value: any, key: str) -> None:
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

    def retrieve_state(self, key: str) -> any:
        try:
            with open(self.file_path, "r") as read_file:
                d = json.load(read_file)
                return d.get(key)
        except (JSONDecodeError, FileNotFoundError):
            return {}


class State:
    """
    The class provides application state persistence
    to continue running after the program stops.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Set the state to a specific key"""
        self.storage.save_state(value, key)

    def get_state(self, key: str) -> Any:
        """Get the state from a specific key"""
        return self.storage.retrieve_state(key)


class FakeState:
    """Development tool"""
    def set_state(self, key: str, value: Any) -> None:
        pass

    def get_state(self, key: str) -> Any:
        return {'last_modified': '1000-10-10'}


if settings.USE_STATE:
    logger.info('The programm was started in statable mode.')
    state = State(JsonFileStorage(settings.STATE_FILE_PATH))
else:
    logger.info('The programm was started without state handling.')
    state = FakeState()
