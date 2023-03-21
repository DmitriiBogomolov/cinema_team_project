import os
from logging import config as logging_config
from dotenv import load_dotenv

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(os.path.dirname(BASE_DIR), '.env'))

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 2))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

PIT_MAX_AGE = 20  # in seconds
USE_PIT_ROTATION = True
