from jwt.exceptions import InvalidTokenError


class RevokedTokenError(InvalidTokenError):
    """Called if the token is in blocklist"""
    pass


class AlreadyExistsError(Exception):
    """Called if the user already exist"""
    pass
