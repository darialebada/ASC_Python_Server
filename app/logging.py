""" logging.py """
import time
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = RotatingFileHandler("app/webserver.log", maxBytes=1024 * 1024, backupCount=10)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# convert time to UTC/GMT format
formatter.converter = time.gmtime

handler.setFormatter(formatter)
# add handler to logger
logger.addHandler(handler)
