#!/usr/bin/env python
""" generated source for module Order """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib import Double, Integer
from ib.ext.Util import Util
# 
#  * Order.java
#  *
#  
# package: com.ib.client


class Order(object):
    """ generated source for class Order """
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

    #  main order fields
    m_orderId = 0
    m_clientId = 0
    m_permId = 0
    m_action = ""
    m_totalQuantity = 0
    m_orderType = ""
    m_lmtPrice = float()
    m_auxPrice = float()

    #  extended order fields
    m_tif = ""  #  "Time in Force" - DAY, GTC, etc.
    m_activeStartTime = ""  #  GTC orders
    m_activeStopTime = ""  #  GTC orders
    m_ocaGroup = "" #  one cancels all group name
    m_ocaType = 0   #  1 = CANCEL_WITH_BLOCK, 2 = REDUCE_WITH_BLOCK, 3 = REDUCE_NON_BLOCK
    m_orderRef = ""
    m_transmit = bool() #  if false, order will be created but not transmited
    m_parentId = 0  #  Parent order Id, to associate Auto STP or TRAIL orders with the original order.
    m_blockOrder = bool()
    m_sweepToFill = bool()
    m_displaySize = 0
    m_triggerMethod = 0 #  0=Default, 1=Double_Bid_Ask, 2=Last, 3=Double_Last, 4=Bid_Ask, 7=Last_or_Bid_Ask, 8=Mid-point
    m_outsideRth = bool()
    m_hidden = bool()
    m_goodAfterTime = ""    #  FORMAT: 20060505 08:00:00 {time zone}
    m_goodTillDate = ""     #  FORMAT: 20060505 08:00:00 {time zone}
    m_overridePercentageConstraints = bool()
    m_rule80A = ""  #  Individual = 'I', Agency = 'A', AgentOtherMember = 'W', IndividualPTIA = 'J', AgencyPTIA = 'U', AgentOtherMemberPTIA = 'M', IndividualPT = 'K', AgencyPT = 'Y', AgentOtherMemberPT = 'N'
    m_allOrNone = bool()
    m_minQty = 0
    m_percentOffset = float()   #  REL orders only; specify the decimal, e.g. .04 not 4
    m_trailStopPrice = float()  #  for TRAILLIMIT orders only
    m_trailingPercent = float()  #  specify the percentage, e.g. 3, not .03

    #  Financial advisors only 
    m_faGroup = ""
    m_faProfile = ""
    m_faMethod = ""
    m_faPercentage = ""

    #  Institutional orders only
    m_openClose = ""            #  O=Open, C=Close
    m_origin = 0                #  0=Customer, 1=Firm
    m_shortSaleSlot = 0         #  1 if you hold the shares, 2 if they will be delivered from elsewhere.  Only for Action="SSHORT
    m_designatedLocation = ""   #  set when slot=2 only.
    m_exemptCode = 0

    #  SMART routing only
    m_discretionaryAmt = float()
    m_eTradeOnly = bool()
    m_firmQuoteOnly = bool()
    m_nbboPriceCap = float()
    m_optOutSmartRouting = bool()

    #  BOX or VOL ORDERS ONLY
    m_auctionStrategy = 0   #  1=AUCTION_MATCH, 2=AUCTION_IMPROVEMENT, 3=AUCTION_TRANSPARENT

    
    #  BOX ORDERS ONLY
    m_startingPrice = float()
    m_stockRefPrice = float()
    m_delta = float()

    #  pegged to stock or VOL orders
    m_stockRangeLower = float()
    m_stockRangeUpper = float()

    #  VOLATILITY ORDERS ONLY
    m_volatility = float()  #  enter percentage not decimal, e.g. 2 not .02
    m_volatilityType = 0        #  1=daily, 2=annual
    m_continuousUpdate = 0
    m_referencePriceType = 0    #  1=Bid/Ask midpoint, 2 = BidOrAsk
    m_deltaNeutralOrderType = ""
    m_deltaNeutralAuxPrice = float()
    m_deltaNeutralConId = 0
    m_deltaNeutralSettlingFirm = ""
    m_deltaNeutralClearingAccount = ""
    m_deltaNeutralClearingIntent = ""
    m_deltaNeutralOpenClose = ""
    m_deltaNeutralShortSale = bool()
    m_deltaNeutralShortSaleSlot = 0
    m_deltaNeutralDesignatedLocation = ""

    #  COMBO ORDERS ONLY
    m_basisPoints = float() #  EFP orders only, download only
    m_basisPointsType = 0   #  EFP orders only, download only
    
    #  SCALE ORDERS ONLY
    m_scaleInitLevelSize = 0
    m_scaleSubsLevelSize = 0
    m_scalePriceIncrement = float()
    m_scalePriceAdjustValue = float()
    m_scalePriceAdjustInterval = 0
    m_scaleProfitOffset = float()
    m_scaleAutoReset = bool()
    m_scaleInitPosition = 0
    m_scaleInitFillQty = 0
    m_scaleRandomPercent = bool()
    m_scaleTable = ""

    #  HEDGE ORDERS ONLY
    m_hedgeType = ""    #  'D' - delta, 'B' - beta, 'F' - FX, 'P' - pair
    m_hedgeParam = ""   #  beta value for beta hedge (in range 0-1), ratio for pair hedge
    
    #  Clearing info
    m_account = ""          #  IB account
    m_settlingFirm = ""
    m_clearingAccount = ""  #  True beneficiary of the order
    m_clearingIntent = ""   #  "" (Default), "IB", "Away", "PTA" (PostTrade)

    #  ALGO ORDERS ONLY
    m_algoStrategy = ""
    m_algoParams = None

    #  What-if
    m_whatIf = bool()

    #  Not Held
    m_notHeld = bool()

    #  Smart combo routing params
    m_smartComboRoutingParams = None

    #  order combo legs
    m_orderComboLegs = []

    def __init__(self):
        """ generated source for method __init__ """
        self.m_lmtPrice = Double.MAX_VALUE
        self.m_auxPrice = Double.MAX_VALUE
        self.m_activeStartTime = self.EMPTY_STR
        self.m_activeStopTime = self.EMPTY_STR
        self.m_outsideRth = False
        self.m_openClose = "O"
        self.m_origin = self.CUSTOMER
        self.m_transmit = True
        self.m_designatedLocation = self.EMPTY_STR
        self.m_exemptCode = -1
        self.m_minQty = Integer.MAX_VALUE
        self.m_percentOffset = Double.MAX_VALUE
        self.m_nbboPriceCap = Double.MAX_VALUE
        self.m_optOutSmartRouting = False
        self.m_startingPrice = Double.MAX_VALUE
        self.m_stockRefPrice = Double.MAX_VALUE
        self.m_delta = Double.MAX_VALUE
        self.m_stockRangeLower = Double.MAX_VALUE
        self.m_stockRangeUpper = Double.MAX_VALUE
        self.m_volatility = Double.MAX_VALUE
        self.m_volatilityType = Integer.MAX_VALUE
        self.m_deltaNeutralOrderType = self.EMPTY_STR
        self.m_deltaNeutralAuxPrice = Double.MAX_VALUE
        self.m_deltaNeutralConId = 0
        self.m_deltaNeutralSettlingFirm = self.EMPTY_STR
        self.m_deltaNeutralClearingAccount = self.EMPTY_STR
        self.m_deltaNeutralClearingIntent = self.EMPTY_STR
        self.m_deltaNeutralOpenClose = self.EMPTY_STR
        self.m_deltaNeutralShortSale = False
        self.m_deltaNeutralShortSaleSlot = 0
        self.m_deltaNeutralDesignatedLocation = self.EMPTY_STR
        self.m_referencePriceType = Integer.MAX_VALUE
        self.m_trailStopPrice = Double.MAX_VALUE
        self.m_trailingPercent = Double.MAX_VALUE
        self.m_basisPoints = Double.MAX_VALUE
        self.m_basisPointsType = Integer.MAX_VALUE
        self.m_scaleInitLevelSize = Integer.MAX_VALUE
        self.m_scaleSubsLevelSize = Integer.MAX_VALUE
        self.m_scalePriceIncrement = Double.MAX_VALUE
        self.m_scalePriceAdjustValue = Double.MAX_VALUE
        self.m_scalePriceAdjustInterval = Integer.MAX_VALUE
        self.m_scaleProfitOffset = Double.MAX_VALUE
        self.m_scaleAutoReset = False
        self.m_scaleInitPosition = Integer.MAX_VALUE
        self.m_scaleInitFillQty = Integer.MAX_VALUE
        self.m_scaleRandomPercent = False
        self.m_scaleTable = self.EMPTY_STR
        self.m_whatIf = False
        self.m_notHeld = False

    def __eq__(self, p_other):
        """ generated source for method equals """
        if self is p_other:
            return True
        if p_other is None:
            return False
        l_theOther = p_other
        if self.m_permId == l_theOther.m_permId:
            return True
        if self.m_orderId != l_theOther.m_orderId or self.m_clientId != l_theOther.m_clientId or self.m_totalQuantity != l_theOther.m_totalQuantity or self.m_lmtPrice != l_theOther.m_lmtPrice or self.m_auxPrice != l_theOther.m_auxPrice or self.m_ocaType != l_theOther.m_ocaType or self.m_transmit != l_theOther.m_transmit or self.m_parentId != l_theOther.m_parentId or self.m_blockOrder != l_theOther.m_blockOrder or self.m_sweepToFill != l_theOther.m_sweepToFill or self.m_displaySize != l_theOther.m_displaySize or self.m_triggerMethod != l_theOther.m_triggerMethod or self.m_outsideRth != l_theOther.m_outsideRth or self.m_hidden != l_theOther.m_hidden or self.m_overridePercentageConstraints != l_theOther.m_overridePercentageConstraints or self.m_allOrNone != l_theOther.m_allOrNone or self.m_minQty != l_theOther.m_minQty or self.m_percentOffset != l_theOther.m_percentOffset or self.m_trailStopPrice != l_theOther.m_trailStopPrice or self.m_trailingPercent != l_theOther.m_trailingPercent or self.m_origin != l_theOther.m_origin or self.m_shortSaleSlot != l_theOther.m_shortSaleSlot or self.m_discretionaryAmt != l_theOther.m_discretionaryAmt or self.m_eTradeOnly != l_theOther.m_eTradeOnly or self.m_firmQuoteOnly != l_theOther.m_firmQuoteOnly or self.m_nbboPriceCap != l_theOther.m_nbboPriceCap or self.m_optOutSmartRouting != l_theOther.m_optOutSmartRouting or self.m_auctionStrategy != l_theOther.m_auctionStrategy or self.m_startingPrice != l_theOther.m_startingPrice or self.m_stockRefPrice != l_theOther.m_stockRefPrice or self.m_delta != l_theOther.m_delta or self.m_stockRangeLower != l_theOther.m_stockRangeLower or self.m_stockRangeUpper != l_theOther.m_stockRangeUpper or self.m_volatility != l_theOther.m_volatility or self.m_volatilityType != l_theOther.m_volatilityType or self.m_continuousUpdate != l_theOther.m_continuousUpdate or self.m_referencePriceType != l_theOther.m_referencePriceType or self.m_deltaNeutralAuxPrice != l_theOther.m_deltaNeutralAuxPrice or self.m_deltaNeutralConId != l_theOther.m_deltaNeutralConId or self.m_deltaNeutralShortSale != l_theOther.m_deltaNeutralShortSale or self.m_deltaNeutralShortSaleSlot != l_theOther.m_deltaNeutralShortSaleSlot or self.m_basisPoints != l_theOther.m_basisPoints or self.m_basisPointsType != l_theOther.m_basisPointsType or self.m_scaleInitLevelSize != l_theOther.m_scaleInitLevelSize or self.m_scaleSubsLevelSize != l_theOther.m_scaleSubsLevelSize or self.m_scalePriceIncrement != l_theOther.m_scalePriceIncrement or self.m_scalePriceAdjustValue != l_theOther.m_scalePriceAdjustValue or self.m_scalePriceAdjustInterval != l_theOther.m_scalePriceAdjustInterval or self.m_scaleProfitOffset != l_theOther.m_scaleProfitOffset or self.m_scaleAutoReset != l_theOther.m_scaleAutoReset or self.m_scaleInitPosition != l_theOther.m_scaleInitPosition or self.m_scaleInitFillQty != l_theOther.m_scaleInitFillQty or self.m_scaleRandomPercent != l_theOther.m_scaleRandomPercent or self.m_whatIf != l_theOther.m_whatIf or self.m_notHeld != l_theOther.m_notHeld or self.m_exemptCode != l_theOther.m_exemptCode:
            return False
        if Util.StringCompare(self.m_action, l_theOther.m_action) != 0 or Util.StringCompare(self.m_orderType, l_theOther.m_orderType) != 0 or Util.StringCompare(self.m_tif, l_theOther.m_tif) != 0 or Util.StringCompare(self.m_activeStartTime, l_theOther.m_activeStartTime) != 0 or Util.StringCompare(self.m_activeStopTime, l_theOther.m_activeStopTime) != 0 or Util.StringCompare(self.m_ocaGroup, l_theOther.m_ocaGroup) != 0 or Util.StringCompare(self.m_orderRef, l_theOther.m_orderRef) != 0 or Util.StringCompare(self.m_goodAfterTime, l_theOther.m_goodAfterTime) != 0 or Util.StringCompare(self.m_goodTillDate, l_theOther.m_goodTillDate) != 0 or Util.StringCompare(self.m_rule80A, l_theOther.m_rule80A) != 0 or Util.StringCompare(self.m_faGroup, l_theOther.m_faGroup) != 0 or Util.StringCompare(self.m_faProfile, l_theOther.m_faProfile) != 0 or Util.StringCompare(self.m_faMethod, l_theOther.m_faMethod) != 0 or Util.StringCompare(self.m_faPercentage, l_theOther.m_faPercentage) != 0 or Util.StringCompare(self.m_openClose, l_theOther.m_openClose) != 0 or Util.StringCompare(self.m_designatedLocation, l_theOther.m_designatedLocation) != 0 or Util.StringCompare(self.m_deltaNeutralOrderType, l_theOther.m_deltaNeutralOrderType) != 0 or Util.StringCompare(self.m_deltaNeutralSettlingFirm, l_theOther.m_deltaNeutralSettlingFirm) != 0 or Util.StringCompare(self.m_deltaNeutralClearingAccount, l_theOther.m_deltaNeutralClearingAccount) != 0 or Util.StringCompare(self.m_deltaNeutralClearingIntent, l_theOther.m_deltaNeutralClearingIntent) != 0 or Util.StringCompare(self.m_deltaNeutralOpenClose, l_theOther.m_deltaNeutralOpenClose) != 0 or Util.StringCompare(self.m_deltaNeutralDesignatedLocation, l_theOther.m_deltaNeutralDesignatedLocation) != 0 or Util.StringCompare(self.m_hedgeType, l_theOther.m_hedgeType) != 0 or Util.StringCompare(self.m_hedgeParam, l_theOther.m_hedgeParam) != 0 or Util.StringCompare(self.m_account, l_theOther.m_account) != 0 or Util.StringCompare(self.m_settlingFirm, l_theOther.m_settlingFirm) != 0 or Util.StringCompare(self.m_clearingAccount, l_theOther.m_clearingAccount) != 0 or Util.StringCompare(self.m_clearingIntent, l_theOther.m_clearingIntent) != 0 or Util.StringCompare(self.m_algoStrategy, l_theOther.m_algoStrategy) != 0 or Util.StringCompare(self.m_scaleTable, l_theOther.m_scaleTable) != 0:
            return False
        if not Util.VectorEqualsUnordered(self.m_algoParams, l_theOther.m_algoParams):
            return False
        if not Util.VectorEqualsUnordered(self.m_smartComboRoutingParams, l_theOther.m_smartComboRoutingParams):
            return False
        #  compare order combo legs
        if not Util.VectorEqualsUnordered(self.m_orderComboLegs, l_theOther.m_orderComboLegs):
            return False
        return True

