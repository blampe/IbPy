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
                 exec_id='',
                 time='',
                 acct_number='',
                 exchange='',
                 side='',
                 shares=0, 
                 price=0.0, 
                 permId=0,
                 liquidation=0):
        setattr_mapping(self, locals())
