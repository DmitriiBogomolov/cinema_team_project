import logging


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(request_id)s'

logger = logging.getLogger('ugc')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/ugc.log')
formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)

logger.addHandler(handler)
