#!/usr/bin/env python
""" Defines the ExecutionFilter class.

"""
from ib.lib import setattr_mapping


class ExecutionFilter(object):
    """ ExecutionFilter -> what's an execution filter?

    """
    def __init__(self,
                 clientId=0,
                 acct_code='',
                 time='',
                 symbol='',
                 secType='',
                 exchange='',
                 side=''):
        setattr_mapping(self, locals())
