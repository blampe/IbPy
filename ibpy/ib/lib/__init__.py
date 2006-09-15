#!/usr/bin/env python
""" ib.lib -> library for bits used elsewhere in this package.

"""
import logging
import os
import sys

logger_format = '%(asctime)s %(module)s.py:%(lineno)d %(levelname)-9.9s %(message)s'
logger_date_format = '%d-%b-%y %H:%M:%S'
logger_level = int(os.environ.get('IBPY_LOGLEVEL', logging.DEBUG))


def logger(name='IbPy', level=logger_level, format=logger_format,
           date_format=logger_date_format):
    """ logger(level) -> returns a logger all fixed up

    """
    if sys.version_info[0:2] < (2, 4):
        logging.basicConfig()
        logger = logging.getLogger(name)
        logger.setLevel(logger_level)
        formatter = logging.Formatter(logger_format, logger_date_format)
        for handler in logger.handlers:
            handler.setFormatter(formatter)
            handler.setLevel(logger_level)
        return logger
    else:
        logging.basicConfig(level=level,
                            format=format,
                            datefmt=date_format)
        return logging


def getattrs(obj, seq):
    values = [getattr(obj, k) for k in seq]
    try:
        return [v.lower() for v in values]
    except (AttributeError, ):
        return values


def setattr_mapping(obj, mapping):
    """ setattr_mapping(object, mapping) -> add attributes from mapping to obj

    """
    del(mapping['self'])
    obj.__dict__.update(mapping)
