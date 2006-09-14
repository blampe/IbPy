#!/usr/bin/env python
""" Defines the ExecutionDetails class.

"""
from ib.lib import setattr_mapping


class ExecutionDetails(object):
    """ ExecutionDetails(...) -> execution details 

    """
    def __init__(self, 
                 order_id=0,
                 client_id=0,
                 exec_id='',
                 time='',
                 acct_number='',
                 exchange='',
                 side='',
                 shares=0, 
                 price=0.0, 
                 perm_id=0,
                 liquidation=0):
        setattr_mapping(self, locals())
