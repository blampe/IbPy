#!/usr/bin/env python
""" Ib.Type -> data types

"""
class ComboLeg(object):
    """ ComboLeg(...) -> a combo leg
        
        same = 0
        open = 1
        close = 2
        unknown = 3
    """
    def __init__(self,
                 con_id=0,
                 ratio=0,
                 action='',
                 exchange='',
                 open_close=0):

        setattr_mapping(self, locals())


class Contract(object):
    """ Contract(...) -> a stock or option contract 

    """
    def __init__(self,
                 symbol='',
                 sec_type='',
                 expiry='',
                 strike=0.0,
                 right='',
                 exchange='SMART',
                 currency='', 
                 local_symbol='',
                 combo_legs=None):

        if combo_legs is None:
            combo_legs = []

        setattr_mapping(self, locals())


class ContractDetails(object):
    """ ContractDetails(...) -> contract details 

    """
    def __init__(self,
                 market_name='', 
                 trading_class='', 
                 con_id=0, 
                 min_tick=0.0,
                 multiplier='', 
                 order_types='', 
                 valid_exchanges='',
                 summary=None):

        if summary is None:
            summary = Contract()

        setattr_mapping(self, locals())


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
                 perm_id=0):

        setattr_mapping(self, locals())


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


class Order(object):
    """ Order(...) -> an order 

    """
    def __init__(self, 
                 order_id=0,
                 client_id=0,
                 action='BUY',
                 quantity=0, 
                 order_type='LMT', 
                 limit_price=0, 
                 aux_price=0, 
                 shares_allocation='',
                 tif='DAY', 
                 oca_group='',
                 account='', 
                 open_close='O',
                 origin=0,
                 order_ref='',
                 transmit=1, 
                 parent_id=0,
                 block_order=0,
                 sweep_to_fill=0,
                 display_size=0,
                 trigger_method=1,
                 ignore_rth=0,
                 hidden=0):

        origin_customer = 0
        origin_firm = 1
        setattr_mapping(self, locals())


def setattr_mapping(obj, mapping):
    """ setattr_mapping(object, mapping) -> add attributes from mapping to obj

    """
    del mapping['self']
    obj.__dict__.update(mapping)
