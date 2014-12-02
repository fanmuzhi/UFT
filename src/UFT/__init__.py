import logging
from logger_handler import init_logger

formatter = logging.Formatter('[ %(asctime)s ] (%(threadName)s)'
                              ' %(module)s : %(message)s')
logger = logging.getLogger(__name__)
init_logger(logger, formatter, logging.INFO)
