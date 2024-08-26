import logging

from .defaults import LOGGING_FILE

logging.basicConfig(
    level="INFO",
    filename=LOGGING_FILE,
    style="{",
    format="{asctime} - {levelname}({levelno}) : {filename}(Line {lineno}) : {message}",
)


def logger(name=None):
    return logging.getLogger(name)
