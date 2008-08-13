#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines logging formats and logger instance
##

import logging
import os

##
# Default log message formatting string.
format = '%(asctime)s %(levelname)-9.9s %(message)s'

##
# Default log date formatting string.
datefmt = '%d-%b-%y %H:%M:%S'

##
# Default log level.  Set IBPY_LOGLEVEL environment variable to
# change this default.
level = int(os.environ.get('IBPY_LOGLEVEL', logging.DEBUG))


def logger(name='ibpy', level=level, format=format,
               datefmt=datefmt):
    """ Configures and returns a logging instance.

    @param name ignored
    @param level logging level
    @param format format string for log messages
    @param datefmt format string for log dates
    @return logging instance (the module)
    """
    logging.basicConfig(level=level, format=format, datefmt=datefmt)
    return logging.getLogger(name)
