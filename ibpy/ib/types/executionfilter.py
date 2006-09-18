#!/usr/bin/env python
""" Defines the ExecutionFilter class.

"""
from ib.lib import getattrs, setattrs


class ExecutionFilter(object):
    """ ExecutionFilter -> what's an execution filter?

    """
    def __init__(self,
                 clientId=0,
                 acctCode='',
                 time='',
                 symbol='',
                 secType='',
                 exchange='',
                 side=''):
        setattrs(self, locals())

    def __eq__(self, other):
        if other is None:
            return False
        if self is other:
            return True
        syms = ('acctCode', 'time', 'symbol', 'secType', 'exchange', 'side')
        return getattrs(self, syms) == getattrs(other, syms)
