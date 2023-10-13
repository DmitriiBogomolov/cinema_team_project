import logging
import os


if not os.path.isdir('logs'):
    os.mkdir('logs')

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logger = logging.getLogger('notification_worker')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/notification_worker.log')
formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)

logger.addHandler(handler)
