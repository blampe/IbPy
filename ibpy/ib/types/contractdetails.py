#!/usr/bin/env python
""" Defines the ContracDetails class.

"""
from ib.lib import setattr_mapping


class ContractDetails(object):
    """ ContractDetails(...) -> contract details 

    """
    def __init__(self,
                 summary=None,
                 market_name='', 
                 trading_class='', 
                 con_id=0, 
                 min_tick=0.0,
                 multiplier='',
                 order_types='', 
                 valid_exchanges=''):
        if summary is None:
            summary = Contract()
        price_magnifier = 1
        setattr_mapping(self, locals())

    def __str__(self):
        return 'Details(%s)' % (self.summary, )
