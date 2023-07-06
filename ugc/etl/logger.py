import logging


LOG_FORMAT = '%(asctime)s: %(lineno)s-%(levelname)s-%(message)s'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formater = logging.Formatter(LOG_FORMAT)
handler = logging.FileHandler('etl.log', mode='w')
handler.setFormatter(formater)
logger.addHandler(handler)
