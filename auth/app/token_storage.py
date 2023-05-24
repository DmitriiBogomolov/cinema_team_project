from abc import ABC, abstractmethod
import uuid

from app.extensions import redis_db


class AbstractTokenStorage(ABC):
    """Token storage"""
    @abstractmethod
    def save_user_token(user_id: uuid, token: dict) -> None:
        pass

    @abstractmethod
    def check_user_token(user_id: uuid, jti: str) -> bool:
        """Checks if the token with ID in storage"""
        pass

    @abstractmethod
    def get_user_token(user_id: uuid, jti: str) -> dict:
        """Gets certain user token"""
        pass

    @abstractmethod
    def delete_user_token(user_id: uuid, token: dict) -> bool:
        """Deletes certain user token"""
        pass

    @abstractmethod
    def get_all_user_tokens(user_id: uuid) -> list[dict]:
        """Gets all user tokens"""
        pass

    @abstractmethod
    def delete_all_user_tokens(user_id: uuid) -> int:
        """Deletes all user tokens"""
        pass


class RedisTokenStorage(AbstractTokenStorage):
    """Uses {prefix} notation to associate a user with tokens.
        More about notation https://redis.io/topics/cluster-tutorial"""
    def save_user_token(self, user_id: uuid, token: dict) -> None:
        key = '{%s}%s' % (user_id, token['jti'])
        redis_db.hmset(key, token)

    def check_user_token(self, user_id: uuid, jti: str) -> bool:
        key = '{%s}%s' % (user_id, jti)
        return bool(redis_db.exists(key))

    def get_user_token(self, user_id: uuid, jti: str) -> dict:
        key = '{%s}%s' % (user_id, jti)
        return redis_db.hgetall(key)

    def delete_user_token(self, user_id: uuid, jti: str) -> bool:
        key = '{%s}%s' % (user_id, jti)
        return bool(redis_db.delete(key))

    def get_all_user_tokens(self, user_id: uuid) -> list[dict]:
        keys = redis_db.scan_iter('{%s}*' % user_id)
        return [redis_db.hgetall(key) for key in keys]

    def delete_all_user_tokens(self, user_id: uuid) -> int:
        keys = list(redis_db.scan_iter('{%s}*' % user_id))
        for key in keys:
            redis_db.delete(key)
        return len(keys)


token_storage = RedisTokenStorage()
