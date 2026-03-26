import logging
import os
import sys


from dotenv import load_dotenv

load_dotenv()

PROGNAME = "dsprofile"

USE_LOGGING = os.getenv("DSPROFILE_USE_LOGGING", "0") != "0"

def log_config(log_level="INFO"):
    logger = logging.getLogger(PROGNAME)
    if USE_LOGGING:
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("{asctime} [{name}] {levelname} {message}",
                                      datefmt="%Y-%m-%d %H:%M:%S", style='{')
        handler.setFormatter(formatter)
    else:
        handler = logging.NullHandler()

    logger.addHandler(handler)


def getLogger():
    return logging.getLogger(PROGNAME)
