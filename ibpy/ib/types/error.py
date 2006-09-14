#!/usr/bin/env python
""" Defines the Error class.

"""
from ib.lib import setattr_mapping


class Error(object):
    """ Error(...) -> client error type

    """
    def __init__(self, code=0, msg=''):
        setattr_mapping(locals())
