import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('my_logger')
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler('log/file.log',
                            maxBytes=2000,
                            backupCount=10
                            )
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug('hello')