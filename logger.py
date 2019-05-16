import logging


def logger_initializing(logging_level):
    _logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)
    _logger.setLevel(getattr(logging, logging_level))
    return _logger


logger = logger_initializing("INFO")
