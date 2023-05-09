import logging
import sys


from src.utils.colorlevel import ColorLevel

def get_logger(name):
    handler = logging.StreamHandler(sys.stdout)
    _logger = logging.Logger(name)

    formatter = ColorLevel()
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    return _logger
