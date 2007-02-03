#!/usr/bin/env python
""" Defines the Order class.

"""
from ib.lib import getattrs, maxint, maxfloat, setattrs


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
    OPT_SPECIALIST= 'y'
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

        ## extended order fields
        tif='DAY',  ## "Time in Force" - DAY, GTC, etc.
        ocaGroup='', ## one cancels all group name
        ocaType=1,  ## 1 = CANCEL_WITH_BLOCK, 2 = REDUCE_WITH_BLOCK, 3 = REDUCE_NON_BLOCK
        orderRef='',
        transmit=1,	## if false, order will be created but not transmited
        parentId=0,	## Parent order Id, to associate Auto STP or TRAIL orders with the original order.
        blockOrder=0,
        sweepToFill=0,
        displaySize=0,
        triggerMethod=0, ## 0=Default, 1=Double_Bid_Ask, 2=Last, 3=Double_Last, 4=Bid_Ask, 7=Last_or_Bid_Ask, 8=Mid-point
        ignoreRth=0,
        hidden=0,
        goodAfterTime='', ## FORMAT: 20060505 08:00:00 {time zone}
        goodTillDate='',  ## FORMAT: 20060505 08:00:00 {time zone}
        rthOnly=0,
        overridePercentageConstraints=0,
        rule80A='A',  ## Individual = 'I', Agency = 'A', AgentOtherMember = 'W', IndividualPTIA = 'J', AgencyPTIA = 'U', AgentOtherMemberPTIA = 'M', IndividualPT = 'K', AgencyPT = 'Y', AgentOtherMemberPT = 'N'
        allOrNone=1,
        minQty=maxint,
        percentOffset=maxfloat, ## REL orders only
        trailStopPrice=maxfloat, ## for TRAILLIMIT orders only
        sharesAllocation='', ## deprecated

        ## Financial advisors only 
        faGroup='',
        faProfile='',
        faMethod='',
        faPercentage='',

        ## Institutional orders only
        account='',
        settlingFirm='',
        openClose='O',          ## O=Open, C=Close
        origin=1,             ## 0=Customer, 1=Firm
        shortSaleSlot=1,      ## 1 if you hold the shares, 2 if they will be delivered from elsewhere.  Only for Action="SSHORT
        designatedLocation='', ## set when slot=2 only.

        ## SMART routing only
        discretionaryAmt=0.0,
        eTradeOnly=0,
        firmQuoteOnly=0,
        nbboPriceCap=maxfloat,

        ## BOX or VOL ORDERS ONLY
        auctionStrategy=1, ## 1=AUCTION_MATCH, 2=AUCTION_IMPROVEMENT, 3=AUCTION_TRANSPARENT

        ## BOX ORDERS ONLY
        startingPrice=maxfloat,
        stockRefPrice=maxfloat,
        delta=maxfloat,

        ## pegged to stock or VOL orders
        stockRangeLower=maxfloat,
        stockRangeUpper=maxfloat,

        ## VOLATILITY ORDERS ONLY
        volatility=maxfloat,
        volatilityType=maxint,     ## 1=daily, 2=annual
        continuousUpdate=0,
        referencePriceType=maxint, ## 1=Average, 2 = BidOrAsk
        deltaNeutralOrderType='',
        deltaNeutralAuxPrice=maxfloat,
                 ):
        setattrs(self, locals())
        
                 
    def old__init__(self,
                 ## main order fields
                 orderId=0,
                 clientId=0,
                 permId=0,
                 action='',
                 totalQuantity=0, 
                 orderType='',
                 lmtPrice=0, 
                 auxPrice=0, 

                 # extended order fields
                 tif='DAY', 
                 ocaGroup='',
                 ocaType='',
                 orderRef='',
                 transmit=1,
                 parentId=0,
                 blockOrder=0,
                 sweepToFill=0,
                 displaySize=0,
                 triggerMethod=1,
                 ignoreRth=0,
                 hidden=0,
                 goodAfterTime='',
                 goodTillDate='',
                 
                 account='', 
                 openClose='O',
                 origin=CUSTOMER,
                 sharesAllocation='',

                 discretionaryAmt=0,
                 faGroup='',
                 faProfile='',
                 faMethod='',
                 faPercentage='',
                 primaryExch='',
                 shortSaleSlot=0,
                 designatedLocation='',

                 overridePercentageConstraints=0,                 
                 rule80A='',
                 settlingFirm='',
                 allOrNone=0,
                 minQty=maxint,
                 percentOffset=maxfloat,
                 eTradeOnly=1,
                 firmQuoteOnly=1,
                 nbboPriceCap=maxfloat,

                 # box orders
                 auctionStrategy=0,
                 startingPrice=maxfloat,
                 stockRefPrice=maxfloat,
                 delta=maxfloat,
                 stockRangeLower=maxfloat,
                 stockRangeUpper=maxfloat,

                 # volatility orders
                 volatility=maxfloat,
                 volatilityType=maxint, # 1=daily, 2=annual
                 continuousUpdate=0,
                 referencePriceType=maxfloat, # 1=average, 2=bidorask
                 deltaNeutralOrderType='',
                 deltaNeutralAuxPrice=maxfloat,
                 ):
        setattrs(self, locals())


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
