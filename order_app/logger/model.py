import logging
from typing import Self


class CustomFormatter(logging.Formatter):
    green = '\033[92m'
    grey = "\x1b[38;20m"
    yellow = '\033[93m'
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[34;20m"
    reset = "\x1b[0m"
    format = "[%(levelname)s] %(asctime)s | %(filename)s | @function %(funcName)s | line %(lineno)s - %(message)s"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class MyLogger:
    logger: Self = None

    @staticmethod
    def get_logger():
        if not MyLogger.logger:
            MyLogger.logger = logging.getLogger('shop_app')
            MyLogger.logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(CustomFormatter())
            MyLogger.logger.addHandler(ch)

        return MyLogger.logger
