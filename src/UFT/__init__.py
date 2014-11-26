import logging
from uft_logger import init_logger

logger = logging.getLogger(__name__)
print __name__
print logger
init_logger(logger, logging.DEBUG)

from cli import test_log
from cli import single_test
