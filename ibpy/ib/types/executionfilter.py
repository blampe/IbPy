#!/usr/bin/env python
""" Defines the ExecutionFilter class.

"""
from ib.lib import setattr_mapping


class ExecutionFilter(object):
    """ ExecutionFilter -> what's an execution filter?

    """
    def __init__(self,
                 client_id=0,
                 acct_code='',
                 time='',
                 symbol='',
                 sec_type='',
                 exchange='',
                 side=''):
        setattr_mapping(self, locals())
