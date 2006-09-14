#!/usr/bin/env python
""" Defines the Order class.

"""
from ib.lib import setattr_mapping, getattrs


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
                 good_after_time='',
                 good_till_date='',

                 fa_group='',
                 fa_profile='',
                 fa_method='',
                 fa_percentage='',
                 primary_exchange='',
                 shortSaleSlot=0,
                 designatedLocation='',

                 ocaType=0,    
                 rthOnly=0,
                 overridePercentageConstraints=0,                 
                 rule80A='',
                 settlingFirm='',
                 allOrNone=0,
                 minQty='',
                 percentOffset='',
                 eTradeOnly=1,
                 firmQuoteOnly=1,
                 nbboPriceCap='',

                 # box orders
                 auctionStrategy='',   
                 startingPrice='',
                 stockRefPrice='',
                 delta='',
                 stockRangeLower='',
                 stockRangeUpper='',

                 # volatility orders
                 volatility=0.0,
                 volatilityType=0, # 1=daily, 2=annual
                 continuousUpdate=0,
                 referencePriceType=0, # 1=average, 2=bidorask
                 deltaNeutralOrderType='',
                 deltaNeutralAuxPrice=0.0,
                 ):
        setattr_mapping(self, locals())

    def __eq__(self, other):
        if self is other:
            return True
        if not other:
            return False
        if self.perm_id == other.perm_id:
            return True
        syms = ('order_id', 'client_id', 'quantity', 'limit_price',
                'aux_price', 'origin', 'transmit', 'parent_id',
                'block_order', 'sweep_to_fill', 'display_size',
                'trigger_method', 'ignore_rth', 'hidden',
                'discretionary_amount', 'shortSaleSlot',
                'designatedLocation', 'ocaType', 'rthOnly',
                'allOrNone', 'minQty', 'percentOffset',
                'eTradeOnly', 'firmQuoteOnly', 'nbboPriceCap',
                'auctionStrategy', 'startingPrice', 'stockRefPrice',
                'delta', 'stockRangeLower', 'stockRangeUpper', 
                'volatility', 'volatilityType', 'deltaNeutralAuxPrice',
                'continuousUpdate', 'referencePriceType')
        if getattrs(self, syms) != getattrs(other, syms):
            return False

        syms = ('order_type', 'tif', 'oca_group', 'account',
                'open_close', 'order_ref', 'good_after_time',
                'good_till_date', 'primary_exchange', 'rule80A',
                'settlingFirm', 'detalNeutralOrderType')
        return getattrs(self, syms) == getattrs(other, syms)
