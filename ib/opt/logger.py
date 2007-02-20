#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.opt.logger -> defines logging formats and logger instance

"""
import logging
import os

format = '%(asctime)s %(levelname)-9.9s %(message)s'
datefmt = '%d-%b-%y %H:%M:%S'
level = int(os.environ.get('IBPY_LOGLEVEL', logging.DEBUG))


def logger(name='ibpy', level=level, format=format,
               datefmt=datefmt):
    """ logger(...) -> returns a logger all fixed up

    """
    logging.basicConfig(level=level, format=format, datefmt=datefmt)
    return logging
