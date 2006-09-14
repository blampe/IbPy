#!/usr/bin/env python
""" Defines the Execution class.

"""
from ib.lib import setattr_mapping


class Execution(object):
    """ Execution(...) -> execution details 

    """
    def __init__(self, 
                 orderId=0,
                 clientId=0,
                 execId='',
                 time='',
                 acctNumber='',
                 exchange='',
                 side='',
                 shares=0, 
                 price=0.0, 
                 permId=0,
                 liquidation=0):
        setattr_mapping(self, locals())


    def __eq__(self, other):
        if other is None:
            return False
        if self is other:
            return True
        return self.execId == other.execId
