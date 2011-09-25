#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for Order.
##

# Source file: Order.java
# Target file: Order.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib import Double, Integer
from ib.ext.Util import Util

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
    m_outsideRth = bool()
    m_hidden = bool()
    m_goodAfterTime = ""
    m_goodTillDate = ""
    m_overridePercentageConstraints = bool()
    m_rule80A = ""
    m_allOrNone = bool()
    m_minQty = 0
    m_percentOffset = float()
    m_trailStopPrice = float()
    m_faGroup = ""
    m_faProfile = ""
    m_faMethod = ""
    m_faPercentage = ""
    m_openClose = ""
    m_origin = 0
    m_shortSaleSlot = 0
    m_designatedLocation = ""
    m_exemptCode = 0
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
    m_basisPoints = float()
    m_basisPointsType = 0
    m_scaleInitLevelSize = 0
    m_scaleSubsLevelSize = 0
    m_scalePriceIncrement = float()
    m_account = ""
    m_settlingFirm = ""
    m_clearingAccount = ""
    m_clearingIntent = ""
    m_algoStrategy = ""
    m_algoParams = list()
    m_whatIf = bool()
    m_notHeld = bool()

    def __init__(self):
        self.m_outsideRth = False
        self.m_openClose = "O"
        self.m_origin = self.CUSTOMER
        self.m_transmit = True
        self.m_designatedLocation = self.EMPTY_STR
        self.m_exemptCode = -1
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
        self.m_basisPoints = Double.MAX_VALUE
        self.m_basisPointsType = Integer.MAX_VALUE
        self.m_scaleInitLevelSize = Integer.MAX_VALUE
        self.m_scaleSubsLevelSize = Integer.MAX_VALUE
        self.m_scalePriceIncrement = Double.MAX_VALUE
        self.m_whatIf = False
        self.m_notHeld = False

    def __eq__(self, p_other):
        if self is p_other:
            return True
        if p_other is None:
            return False
        l_theOther = p_other
        if (self.m_permId == l_theOther.m_permId):
            return True
        if (self.m_orderId != l_theOther.m_orderId) or (self.m_clientId != l_theOther.m_clientId) or (self.m_totalQuantity != l_theOther.m_totalQuantity) or (self.m_lmtPrice != l_theOther.m_lmtPrice) or (self.m_auxPrice != l_theOther.m_auxPrice) or (self.m_ocaType != l_theOther.m_ocaType) or (self.m_transmit != l_theOther.m_transmit) or (self.m_parentId != l_theOther.m_parentId) or (self.m_blockOrder != l_theOther.m_blockOrder) or (self.m_sweepToFill != l_theOther.m_sweepToFill) or (self.m_displaySize != l_theOther.m_displaySize) or (self.m_triggerMethod != l_theOther.m_triggerMethod) or (self.m_outsideRth != l_theOther.m_outsideRth) or (self.m_hidden != l_theOther.m_hidden) or (self.m_overridePercentageConstraints != l_theOther.m_overridePercentageConstraints) or (self.m_allOrNone != l_theOther.m_allOrNone) or (self.m_minQty != l_theOther.m_minQty) or (self.m_percentOffset != l_theOther.m_percentOffset) or (self.m_trailStopPrice != l_theOther.m_trailStopPrice) or (self.m_origin != l_theOther.m_origin) or (self.m_shortSaleSlot != l_theOther.m_shortSaleSlot) or (self.m_discretionaryAmt != l_theOther.m_discretionaryAmt) or (self.m_eTradeOnly != l_theOther.m_eTradeOnly) or (self.m_firmQuoteOnly != l_theOther.m_firmQuoteOnly) or (self.m_nbboPriceCap != l_theOther.m_nbboPriceCap) or (self.m_auctionStrategy != l_theOther.m_auctionStrategy) or (self.m_startingPrice != l_theOther.m_startingPrice) or (self.m_stockRefPrice != l_theOther.m_stockRefPrice) or (self.m_delta != l_theOther.m_delta) or (self.m_stockRangeLower != l_theOther.m_stockRangeLower) or (self.m_stockRangeUpper != l_theOther.m_stockRangeUpper) or (self.m_volatility != l_theOther.m_volatility) or (self.m_volatilityType != l_theOther.m_volatilityType) or (self.m_continuousUpdate != l_theOther.m_continuousUpdate) or (self.m_referencePriceType != l_theOther.m_referencePriceType) or (self.m_deltaNeutralAuxPrice != l_theOther.m_deltaNeutralAuxPrice) or (self.m_basisPoints != l_theOther.m_basisPoints) or (self.m_basisPointsType != l_theOther.m_basisPointsType) or (self.m_scaleInitLevelSize != l_theOther.m_scaleInitLevelSize) or (self.m_scaleSubsLevelSize != l_theOther.m_scaleSubsLevelSize) or (self.m_scalePriceIncrement != l_theOther.m_scalePriceIncrement) or (self.m_whatIf != l_theOther.m_whatIf) or (self.m_notHeld != l_theOther.m_notHeld) or (self.m_exemptCode != l_theOther.m_exemptCode):
            return False
        if (Util.StringCompare(self.m_action, l_theOther.m_action) != 0) or (Util.StringCompare(self.m_orderType, l_theOther.m_orderType) != 0) or (Util.StringCompare(self.m_tif, l_theOther.m_tif) != 0) or (Util.StringCompare(self.m_ocaGroup, l_theOther.m_ocaGroup) != 0) or (Util.StringCompare(self.m_orderRef, l_theOther.m_orderRef) != 0) or (Util.StringCompare(self.m_goodAfterTime, l_theOther.m_goodAfterTime) != 0) or (Util.StringCompare(self.m_goodTillDate, l_theOther.m_goodTillDate) != 0) or (Util.StringCompare(self.m_rule80A, l_theOther.m_rule80A) != 0) or (Util.StringCompare(self.m_faGroup, l_theOther.m_faGroup) != 0) or (Util.StringCompare(self.m_faProfile, l_theOther.m_faProfile) != 0) or (Util.StringCompare(self.m_faMethod, l_theOther.m_faMethod) != 0) or (Util.StringCompare(self.m_faPercentage, l_theOther.m_faPercentage) != 0) or (Util.StringCompare(self.m_openClose, l_theOther.m_openClose) != 0) or (Util.StringCompare(self.m_designatedLocation, l_theOther.m_designatedLocation) != 0) or (Util.StringCompare(self.m_deltaNeutralOrderType, l_theOther.m_deltaNeutralOrderType) != 0) or (Util.StringCompare(self.m_account, l_theOther.m_account) != 0) or (Util.StringCompare(self.m_settlingFirm, l_theOther.m_settlingFirm) != 0) or (Util.StringCompare(self.m_clearingAccount, l_theOther.m_clearingAccount) != 0) or (Util.StringCompare(self.m_clearingIntent, l_theOther.m_clearingIntent) != 0) or (Util.StringCompare(self.m_algoStrategy, l_theOther.m_algoStrategy) != 0):
            return False
        if not Util.VectorEqualsUnordered(self.m_algoParams, l_theOther.m_algoParams):
            return False
        return True


