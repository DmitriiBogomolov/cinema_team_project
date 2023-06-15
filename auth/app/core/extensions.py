import redis
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from app.core.config import config


db = SQLAlchemy()
ma = Marshmallow()

redis_db = redis.StrictRedis(
    host=config.redis_host,
    port=config.redis_port,
    db=0
)

migrate = Migrate()
