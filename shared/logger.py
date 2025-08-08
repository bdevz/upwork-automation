import logging
import sys

from shared.config import settings


def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    return logger

logger = setup_logging("ardan-automation", settings.log_level)
