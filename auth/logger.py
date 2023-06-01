import logging
import logging.handlers
import os
import sys

FORMAT = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'


def init_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(
        filename='./logs/log.log',
        backupCount=1,
        maxBytes=5000
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(sh)
    logger.addHandler(fh)


if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

init_logger('app')
logger = logging.getLogger('app')
