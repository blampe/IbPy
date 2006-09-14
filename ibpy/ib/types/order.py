#!/usr/bin/env python
""" Defines the Order class.

"""
from ib.lib import setattr_mapping, getattrs


class Order(object):
    """ Order(...) -> an order 

    """
    CUSTOMER = 0
    FIRM = 1
    OPT_UNKNOWN = '?'
    OPT_BROKER_DEALER = 'b'
    OPT_CUSTOMER = 'c'
    OPT_FIRM = 'f'
    OPT_ISEMM = 'm'
    OPT_FARMM = 'n'
    OPT_SPECIALIST = 'y'
    AUCTION_MATCH = 1
    AUCTION_IMPROVEMENT = 2
    AUCTION_TRANSPARENT = 3
    EMPTY_STR = ''


    def __init__(self,

                 ## main order fields
                 orderId=0,
                 clientId=0,
                 permId=0,
                 action='',
                 totalQuantity=0, 
                 orderType='',
                 lmtPrice=0, 
                 auxPrice=0, 
                 sharesAllocation='',

                 # extended order fields
                 tif='DAY', 
                 ocaGroup='',
                 account='', 
                 openClose='O',
                 origin=CUSTOMER,
                 orderRef='',
                 transmit=1, 
                 parentId=0,
                 blockOrder=0,
                 sweepToFill=0,
                 displaySize=0,
                 triggerMethod=1,
                 ignoreRth=0,
                 hidden=0,
                 discretionaryAmt=0,
                 goodAfterTime='',
                 goodTillDate='',

                 faGroup='',
                 faProfile='',
                 faMethod='',
                 faPercentage='',
                 primaryExch='',
                 shortSaleSlot=0,
                 designatedLocation='',

                 ocaType=0,    
                 rthOnly=0,
                 overridePercentageConstraints=0,                 
                 rule80A='',
                 settlingFirm='',
                 allOrNone=0,
                 minQty=0,
                 percentOffset=0.0,
                 eTradeOnly=1,
                 firmQuoteOnly=1,
                 nbboPriceCap=0.0,

                 # box orders
                 auctionStrategy=0,
                 startingPrice=0.0,
                 stockRefPrice=0.0,
                 delta=0.0,
                 stockRangeLower=0.0,
                 stockRangeUpper=0.0,

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
        if self.permId == other.permId:
            return True
        syms = ('orderId', 'clientId', 'totalQuantity', 'lmtPrice',
                'auxPrice', 'origin', 'transmit', 'parentId',
                'blockOrder', 'sweepToFill', 'displaySize',
                'triggerMethod', 'ignoreRth', 'hidden',
                'discretionaryAmt', 'shortSaleSlot',
                'designatedLocation', 'ocaType', 'rthOnly',
                'allOrNone', 'minQty', 'percentOffset',
                'eTradeOnly', 'firmQuoteOnly', 'nbboPriceCap',
                'auctionStrategy', 'startingPrice', 'stockRefPrice',
                'delta', 'stockRangeLower', 'stockRangeUpper', 
                'volatility', 'volatilityType', 'deltaNeutralAuxPrice',
                'continuousUpdate', 'referencePriceType')
        if getattrs(self, syms) != getattrs(other, syms):
            return False

        syms = ('orderType', 'tif', 'ocaGroup', 'account',
                'openClose', 'orderRef', 'goodAfterTime',
                'goodTillDate', 'primaryExch', 'rule80A',
                'settlingFirm', 'detalNeutralOrderType')
        return getattrs(self, syms) == getattrs(other, syms)
