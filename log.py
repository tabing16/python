import logging

logger = logging.getLogger()

logging.basicConfig(filename='file.log',
                     level=logging.DEBUG,
                     format='%(levelname)s - %(asctime)s: %(message)s',
                     datefmt='%Y-%m-%d %H:%M:%S',
                     filemode = 'a'
                      )

logger.info("hello")
logger.warning("warning")