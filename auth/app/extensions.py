import redis
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import config

db = SQLAlchemy()
ma = Marshmallow()

redis_db = redis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0
)
