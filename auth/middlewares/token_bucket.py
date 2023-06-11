from typing import Callable
import time
import json

from werkzeug.wrappers import Request, Response

from config import config
from logger import middleware_logger as logger


class TokenBucket:
    """
    Keeps counting the number of tokens a user can utilize to make
    requests in its memory (bucket). Whenever requests are made, tokens
    are reduced from the bucket and fulfilled until tokens are exhausted.
    https://dev.to/satrobit/rate-limiting-using-the-token-bucket-algorithm-3cjh
    """
    def __init__(self,
                 tokens: int,
                 token_increment: int,
                 forward_callback: Callable,
                 drop_callback: Callable):
        """
        tokens: number of tokens in backet.
        token_increment: the number of accumulated tokens every second.
        forward_callback: this function is called when the packet is being forwarded.
        drop_callback: this function is called when the packet should be dropped.
        """
        self.tokens = tokens
        self.token_increment = token_increment
        self.forward_callback = forward_callback
        self.drop_callback = drop_callback
        self.bucket = tokens
        self.last_check = time.time()

    def handle(self, packet):
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current

        self.bucket = self.bucket + \
            time_passed * self.token_increment

        if (self.bucket > self.tokens):
            self.bucket = self.tokens

        if (self.bucket < 1):
            return self.drop_callback(packet)
        else:
            self.bucket = self.bucket - 1
            return self.forward_callback(packet)


class token_bucket_middleware():
    """Provides tocken bucket limiting"""
    def __init__(self, app):
        self.app = app
        self.limiter = TokenBucket(
            config.rate_limit_tokens,
            config.rate_limit_token_increment,
            self._forward,
            self._drop
        )

    def __call__(self, environ, start_response):
        packet = (environ, start_response)
        return self.limiter.handle(packet)

    def _forward(self, packet):
        """Request forwarding callback"""
        environ, start_response = packet
        logger.debug(Request(environ))
        return self.app(environ, start_response)

    def _drop(self, packet):
        """Request dropping callback"""
        environ, start_response = packet
        logger.error('Service overloaded: ' + str(Request(environ)))
        res = Response(
            json.dumps({'message': 'The service overloaded.'}),
            mimetype='application/json',
            status=500
        )
        return res(environ, start_response)
