import logging.config

import hurricane.config

logging.config.fileConfig(hurricane.config.get_resource_path('logger.conf'))


def get_logger(name):
    return logging.getLogger(name)
