import logging
import logging.handlers
import sys
import os

FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'


if not os.path.exists("../logs/"):
    os.makedirs("../logs/")


def init_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(filename='../logs/log.log', backupCount=5, maxBytes=5000)
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(sh)
    logger.addHandler(fh)


init_logger('app')
logger = logging.getLogger('app')
