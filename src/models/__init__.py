import sys
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('[ %(asctime)s ] %(levelname)s %(message)s')

# add stdout handler
stdhl = logging.StreamHandler(sys.stdout)
#stdhl = ColorizingStreamHandler(sys.stdout)
stdhl.setFormatter(formatter)
stdhl.setLevel(logging.DEBUG) # print everything

# add file handler
hdlr = logging.FileHandler("./uft.log")
hdlr.setFormatter(formatter)
hdlr.setLevel(logging.WARNING) # save WARNING, EEROR and CRITICAL to file

# qt handler


logger.addHandler(hdlr)
logger.addHandler(stdhl)
logger.setLevel(logging.DEBUG)
