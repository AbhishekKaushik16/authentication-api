import logging.config


def setup_logger():
    # LOGGING = {
    #     "version": 1,
    #     "disable_existing_loggers": True,
    # }
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    return logger


logger = setup_logger()
