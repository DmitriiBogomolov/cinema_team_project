import logging
import logging.handlers
import os
import sys
from flask import request


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(request_id)s'


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


def init_logger(name, filename, backupCount=1, maxBytes=5000):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    sh.addFilter(RequestIdFilter())
    fh = logging.handlers.RotatingFileHandler(
        filename=filename,
        backupCount=1,
        maxBytes=5000
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.addFilter(RequestIdFilter())
    logger.addHandler(sh)
    logger.addHandler(fh)


if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

init_logger(
    'app',
    './logs/app.log'
)

init_logger(
    'middleware',
    './logs/middleware.log'
)


logger = logging.getLogger('app')
middleware_logger = logging.getLogger('middleware')
