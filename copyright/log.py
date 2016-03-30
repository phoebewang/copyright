import logging

logger = logging.getLogger('root')
FORMAT = "%(asctime)-15s %(filename)s:%(lineno)s %(funcName)s() %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)