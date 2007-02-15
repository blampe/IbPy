#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## Source file: "Order.java"
## Target file: "Order.py"
##
## Original file copyright original author(s).
## This file copyright Troy Melhase <troy@gci.net>.
##

from ib.aux import Integer, Double

class Order(object):
    """ generated source for Order

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
    EMPTY_STR = ""
    m_orderId = 0
    m_clientId = 0
    m_permId = 0
    m_action = ""
    m_totalQuantity = 0
    m_orderType = ""
    m_lmtPrice = float()
    m_auxPrice = float()
    m_tif = ""
    m_ocaGroup = ""
    m_ocaType = 0
    m_orderRef = ""
    m_transmit = bool()
    m_parentId = 0
    m_blockOrder = bool()
    m_sweepToFill = bool()
    m_displaySize = 0
    m_triggerMethod = 0
    m_ignoreRth = bool()
    m_hidden = bool()
    m_goodAfterTime = ""
    m_goodTillDate = ""
    m_rthOnly = bool()
    m_overridePercentageConstraints = bool()
    m_rule80A = ""
    m_allOrNone = bool()
    m_minQty = 0
    m_percentOffset = float()
    m_trailStopPrice = float()
    m_sharesAllocation = ""
    m_faGroup = ""
    m_faProfile = ""
    m_faMethod = ""
    m_faPercentage = ""
    m_account = ""
    m_settlingFirm = ""
    m_openClose = ""
    m_origin = 0
    m_shortSaleSlot = 0
    m_designatedLocation = ""
    m_discretionaryAmt = float()
    m_eTradeOnly = bool()
    m_firmQuoteOnly = bool()
    m_nbboPriceCap = float()
    m_auctionStrategy = 0
    m_startingPrice = float()
    m_stockRefPrice = float()
    m_delta = float()
    m_stockRangeLower = float()
    m_stockRangeUpper = float()
    m_volatility = float()
    m_volatilityType = 0
    m_continuousUpdate = 0
    m_referencePriceType = 0
    m_deltaNeutralOrderType = ""
    m_deltaNeutralAuxPrice = float()

    def __init__(self):
        self.m_openClose = "O"
        self.m_origin = self.CUSTOMER
        self.m_transmit = True
        self.m_designatedLocation = self.EMPTY_STR
        self.m_minQty = Integer.MAX_VALUE
        self.m_percentOffset = Double.MAX_VALUE
        self.m_nbboPriceCap = Double.MAX_VALUE
        self.m_startingPrice = Double.MAX_VALUE
        self.m_stockRefPrice = Double.MAX_VALUE
        self.m_delta = Double.MAX_VALUE
        self.m_stockRangeLower = Double.MAX_VALUE
        self.m_stockRangeUpper = Double.MAX_VALUE
        self.m_volatility = Double.MAX_VALUE
        self.m_volatilityType = Integer.MAX_VALUE
        self.m_deltaNeutralOrderType = self.EMPTY_STR
        self.m_deltaNeutralAuxPrice = Double.MAX_VALUE
        self.m_referencePriceType = Integer.MAX_VALUE
        self.m_trailStopPrice = Double.MAX_VALUE

    def __eq__(self, p_other):
        if self is p_other:
            return True
        else:
            if p_other is None:
                return False
        l_theOther = p_other
        if (self.m_permId == l_theOther.m_permId):
            return True
        firstSetEquals = (self.m_orderId == l_theOther.m_orderId) and (self.m_clientId == l_theOther.m_clientId) and (self.m_totalQuantity == l_theOther.m_totalQuantity) and (self.m_lmtPrice == l_theOther.m_lmtPrice) and (self.m_auxPrice == l_theOther.m_auxPrice) and (self.m_origin == l_theOther.m_origin) and (self.m_transmit == l_theOther.m_transmit) and (self.m_parentId == l_theOther.m_parentId) and (self.m_blockOrder == l_theOther.m_blockOrder) and (self.m_sweepToFill == l_theOther.m_sweepToFill) and (self.m_displaySize == l_theOther.m_displaySize) and (self.m_triggerMethod == l_theOther.m_triggerMethod) and (self.m_ignoreRth == l_theOther.m_ignoreRth) and (self.m_hidden == l_theOther.m_hidden) and (self.m_discretionaryAmt == l_theOther.m_discretionaryAmt) and (self.m_shortSaleSlot == l_theOther.m_shortSaleSlot) and (self.m_designatedLocation == l_theOther.m_designatedLocation) and (self.m_ocaType == l_theOther.m_ocaType) and (self.m_rthOnly == l_theOther.m_rthOnly) and (self.m_allOrNone == l_theOther.m_allOrNone) and (self.m_minQty == l_theOther.m_minQty) and (self.m_percentOffset == l_theOther.m_percentOffset) and (self.m_eTradeOnly == l_theOther.m_eTradeOnly) and (self.m_firmQuoteOnly == l_theOther.m_firmQuoteOnly) and (self.m_nbboPriceCap == l_theOther.m_nbboPriceCap) and (self.m_auctionStrategy == l_theOther.m_auctionStrategy) and (self.m_startingPrice == l_theOther.m_startingPrice) and (self.m_stockRefPrice == l_theOther.m_stockRefPrice) and (self.m_delta == l_theOther.m_delta) and (self.m_stockRangeLower == l_theOther.m_stockRangeLower) and (self.m_stockRangeUpper == l_theOther.m_stockRangeUpper) and (self.m_volatility == l_theOther.m_volatility) and (self.m_volatilityType == l_theOther.m_volatilityType) and (self.m_deltaNeutralAuxPrice == l_theOther.m_deltaNeutralAuxPrice) and (self.m_continuousUpdate == l_theOther.m_continuousUpdate) and (self.m_referencePriceType == l_theOther.m_referencePriceType) and (self.m_trailStopPrice == l_theOther.m_trailStopPrice)
        if not firstSetEquals:
            return False
        else:
            l_thisAction = self.m_action if self.m_action != None else self.EMPTY_STR
            l_thisOrderType = self.m_orderType if self.m_orderType != None else self.EMPTY_STR
            l_thisTif = self.m_tif if self.m_tif != None else self.EMPTY_STR
            l_thisOcaGroup = self.m_ocaGroup if self.m_ocaGroup != None else self.EMPTY_STR
            l_thisAccount = self.m_account if self.m_account != None else self.EMPTY_STR
            l_thisOpenClose = self.m_openClose if self.m_openClose != None else self.EMPTY_STR
            l_thisOrderRef = self.m_orderRef if self.m_orderRef != None else self.EMPTY_STR
            l_thisRule80A = self.m_rule80A if self.m_rule80A != None else self.EMPTY_STR
            l_thisSettlingFirm = self.m_settlingFirm if self.m_settlingFirm != None else self.EMPTY_STR
            l_thisDeltaNeutralOrderType = self.m_deltaNeutralOrderType if self.m_deltaNeutralOrderType != None else self.EMPTY_STR
            l_otherAction = l_theOther.m_action if l_theOther.m_action != None else self.EMPTY_STR
            l_otherOrderType = l_theOther.m_orderType if l_theOther.m_orderType != None else self.EMPTY_STR
            l_otherTif = l_theOther.m_tif if l_theOther.m_tif != None else self.EMPTY_STR
            l_otherOcaGroup = l_theOther.m_ocaGroup if l_theOther.m_ocaGroup != None else self.EMPTY_STR
            l_otherAccount = l_theOther.m_account if l_theOther.m_account != None else self.EMPTY_STR
            l_otherOpenClose = l_theOther.m_openClose if l_theOther.m_openClose != None else self.EMPTY_STR
            l_otherOrderRef = l_theOther.m_orderRef if l_theOther.m_orderRef != None else self.EMPTY_STR
            l_otherOrderGoodAfterTime = l_theOther.m_goodAfterTime if l_theOther.m_goodAfterTime != None else self.EMPTY_STR
            l_otherOrderGoodTillDate = l_theOther.m_goodTillDate if l_theOther.m_goodTillDate != None else self.EMPTY_STR
            l_otherRule80A = l_theOther.m_rule80A if l_theOther.m_rule80A != None else self.EMPTY_STR
            l_otherSettlingFirm = l_theOther.m_settlingFirm if l_theOther.m_settlingFirm != None else self.EMPTY_STR
            l_otherDeltaNeutralOrderType = l_theOther.m_deltaNeutralOrderType if l_theOther.m_deltaNeutralOrderType != None else self.EMPTY_STR
            return l_thisAction == l_otherAction and l_thisOrderType == l_otherOrderType and l_thisTif == l_otherTif and l_thisOcaGroup == l_otherOcaGroup and l_thisAccount == l_otherAccount and l_thisOpenClose == l_otherOpenClose and l_thisOrderRef == l_otherOrderRef and l_otherOrderGoodAfterTime == l_otherOrderGoodAfterTime and l_otherOrderGoodTillDate == l_otherOrderGoodTillDate and l_thisRule80A == l_otherRule80A and l_thisSettlingFirm == l_otherSettlingFirm and l_thisDeltaNeutralOrderType == l_otherDeltaNeutralOrderType


