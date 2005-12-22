#!/usr/bin/env python
""" Ib.Type -> data types

"""
(BID_SIZE, BID_PRICE, ASK_PRICE, ASK_SIZE, LAST_PRICE, LAST_SIZE, HIGH_PRICE,
 LOW_PRICE, VOLUME_SIZE, CLOSE_PRICE) = range(0, 10)


class ComboLeg(object):
    """ ComboLeg(...) -> a combo leg
        
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
                 multiplier='',
                 exchange='SMART',
                 currency='', 
                 local_symbol='',
                 combo_legs=None,
                 primary_exchange=''):
        if combo_legs is None:
            combo_legs = []
        setattr_mapping(self, locals())


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
                 perm_id=0,
                 liquidation=0):
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
    origin_customer = 0
    origin_firm = 1

    def __init__(self,

                 # main order fields
                 order_id=0,
                 client_id=0,
                 perm_id=0,
                 action='BUY',
                 quantity=0, 
                 order_type='LMT', 
                 limit_price=0, 
                 aux_price=0, 
                 shares_allocation='',

                 # extended order fields
                 tif='DAY', 
                 oca_group='',
                 account='', 
                 open_close='O',
                 origin=origin_customer,
                 order_ref='',
                 transmit=1, 
                 parent_id=0,
                 block_order=0,
                 sweep_to_fill=0,
                 display_size=0,
                 trigger_method=1,
                 ignore_rth=0,
                 hidden=0,
                 discretionary_amount=0,
                 good_after_time=0,
                 good_till_date=0,
                 fa_group='',
                 fa_profile='',
                 fa_method='',
                 fa_percentage='',
                 primary_exchange=''):
        setattr_mapping(self, locals())


def setattr_mapping(obj, mapping):
    """ setattr_mapping(object, mapping) -> add attributes from mapping to obj

    """
    del(mapping['self'])
    obj.__dict__.update(mapping)
