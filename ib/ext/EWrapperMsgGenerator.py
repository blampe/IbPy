#!/usr/bin/env python
""" generated source for module EWrapperMsgGenerator """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.ext.AnyWrapperMsgGenerator import AnyWrapperMsgGenerator
from ib.ext.EClientSocket import EClientSocket
from ib.ext.MarketDataType import MarketDataType
from ib.ext.TickType import TickType
from ib.ext.Util import Util

from ib.lib import Double
# package: com.ib.client


class EWrapperMsgGenerator(AnyWrapperMsgGenerator):
    """ generated source for class EWrapperMsgGenerator """
    SCANNER_PARAMETERS = "SCANNER PARAMETERS:"
    FINANCIAL_ADVISOR = "FA:"

    @classmethod
    def tickPrice(cls, tickerId, field, price, canAutoExecute):
        """ generated source for method tickPrice """
        return "id=" + str(tickerId) + "  " + TickType.getField(field) + "=" + str(price) + " " + (" canAutoExecute" if (canAutoExecute != 0) else " noAutoExecute")

    @classmethod
    def tickSize(cls, tickerId, field, size):
        """ generated source for method tickSize """
        return "id=" + str(tickerId) + "  " + TickType.getField(field) + "=" + str(size)

    @classmethod
    def tickOptionComputation(cls, tickerId, field, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        """ generated source for method tickOptionComputation """
        toAdd = "id=" + str(tickerId) + "  " + TickType.getField(field) \
                + ": vol = " + (str(impliedVol) if (impliedVol >= 0 and impliedVol != Double.MAX_VALUE) else "N/A") \
                + " delta = " + (str(delta) if (abs(delta) <= 1) else "N/A") \
                + " gamma = " + (str(gamma) if (abs(gamma) <= 1) else "N/A") \
                + " vega = " + (str(vega) if (abs(vega) <= 1) else "N/A") \
                + " theta = " + (str(theta) if (abs(theta) <= 1) else "N/A") \
                + " optPrice = " + (str(optPrice) if (optPrice >= 0 and optPrice != Double.MAX_VALUE) else "N/A") \
                + " pvDividend = " + (str(pvDividend) if (pvDividend >= 0 and pvDividend != Double.MAX_VALUE) else "N/A") \
                + " undPrice = " + (str(undPrice) if (undPrice >= 0 and undPrice != Double.MAX_VALUE) else "N/A")
        return toAdd

    @classmethod
    def tickGeneric(cls, tickerId, tickType, value):
        """ generated source for method tickGeneric """
        return "id=" + str(tickerId) + "  " + TickType.getField(tickType) + "=" + str(value)

    @classmethod
    def tickString(cls, tickerId, tickType, value):
        """ generated source for method tickString """
        return "id=" + str(tickerId) + "  " + TickType.getField(tickType) + "=" + str(value)

    @classmethod
    def tickEFP(cls, tickerId, tickType, basisPoints, formattedBasisPoints, impliedFuture, holdDays, futureExpiry, dividendImpact, dividendsToExpiry):
        """ generated source for method tickEFP """
        return "id=" + str(tickerId) + "  " + TickType.getField(tickType) \
               + ": basisPoints = " + str(basisPoints) + "/" + formattedBasisPoints \
               + " impliedFuture = " + str(impliedFuture) + " holdDays = " + str(holdDays) \
               + " futureExpiry = " + futureExpiry + " dividendImpact = " + str(dividendImpact) \
               + " dividends to expiry = " + str(dividendsToExpiry)

    @classmethod
    def orderStatus(cls, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld):
        """ generated source for method orderStatus """
        return "order status: orderId=" + str(orderId) + " clientId=" + str(clientId) \
               + " permId=" + str(permId) + " status=" + status + " filled=" + str(filled) \
               + " remaining=" + str(remaining) + " avgFillPrice=" + str(avgFillPrice) \
               + " lastFillPrice=" + str(lastFillPrice) + " parent Id=" + str(parentId) \
               + " whyHeld=" + whyHeld

    @classmethod
    def openOrder(cls, orderId, contract, order, orderState):
        """ generated source for method openOrder """
        msg = "open order: orderId=" + str(orderId) \
              + " action=" + str(order.m_action) \
              + " quantity=" + str(order.m_totalQuantity) \
              + " conid=" + str(contract.m_conId) \
              + " symbol=" + str(contract.m_symbol) \
              + " secType=" + str(contract.m_secType) \
              + " expiry=" + str(contract.m_expiry) \
              + " strike=" + str(contract.m_strike) \
              + " right=" + str(contract.m_right) \
              + " multiplier=" + str(contract.m_multiplier) \
              + " exchange=" + str(contract.m_exchange) \
              + " primaryExch=" + str(contract.m_primaryExch) \
              + " currency=" + str(contract.m_currency) \
              + " localSymbol=" + str(contract.m_localSymbol) \
              + " tradingClass=" + str(contract.m_tradingClass) \
              + " type=" + str(order.m_orderType) \
              + " lmtPrice=" + Util.DoubleMaxString(order.m_lmtPrice) \
              + " auxPrice=" + Util.DoubleMaxString(order.m_auxPrice) \
              + " TIF=" + str(order.m_tif) \
              + " localSymbol=" + str(contract.m_localSymbol) \
              + " client Id=" + str(order.m_clientId) \
              + " parent Id=" + str(order.m_parentId) \
              + " permId=" + str(order.m_permId) \
              + " outsideRth=" + str(order.m_outsideRth) \
              + " hidden=" + str(order.m_hidden) \
              + " discretionaryAmt=" + str(order.m_discretionaryAmt) \
              + " displaySize=" + str(order.m_displaySize) \
              + " triggerMethod=" + str(order.m_triggerMethod) \
              + " goodAfterTime=" + str(order.m_goodAfterTime) \
              + " goodTillDate=" + str(order.m_goodTillDate) \
              + " faGroup=" + str(order.m_faGroup) \
              + " faMethod=" + str(order.m_faMethod) \
              + " faPercentage=" + str(order.m_faPercentage) \
              + " faProfile=" + str(order.m_faProfile) \
              + " shortSaleSlot=" + str(order.m_shortSaleSlot) \
              + " designatedLocation=" + str(order.m_designatedLocation) \
              + " exemptCode=" + str(order.m_exemptCode) \
              + " ocaGroup=" + str(order.m_ocaGroup) \
              + " ocaType=" + str(order.m_ocaType) \
              + " rule80A=" + str(order.m_rule80A) \
              + " allOrNone=" + str(order.m_allOrNone) \
              + " minQty=" + Util.IntMaxString(order.m_minQty) \
              + " percentOffset=" + Util.DoubleMaxString(order.m_percentOffset) \
              + " eTradeOnly=" + order.m_eTradeOnly \
              + " firmQuoteOnly=" + str(order.m_firmQuoteOnly) \
              + " nbboPriceCap=" + Util.DoubleMaxString(order.m_nbboPriceCap) \
              + " optOutSmartRouting=" + str(order.m_optOutSmartRouting) \
              + " auctionStrategy=" + str(order.m_auctionStrategy) \
              + " startingPrice=" + Util.DoubleMaxString(order.m_startingPrice) \
              + " stockRefPrice=" + Util.DoubleMaxString(order.m_stockRefPrice) \
              + " delta=" + Util.DoubleMaxString(order.m_delta) \
              + " stockRangeLower=" + Util.DoubleMaxString(order.m_stockRangeLower) \
              + " stockRangeUpper=" + Util.DoubleMaxString(order.m_stockRangeUpper) \
              + " volatility=" + Util.DoubleMaxString(order.m_volatility) \
              + " volatilityType=" + str(order.m_volatilityType) \
              + " deltaNeutralOrderType=" + str(order.m_deltaNeutralOrderType) \
              + " deltaNeutralAuxPrice=" + Util.DoubleMaxString(order.m_deltaNeutralAuxPrice) \
              + " deltaNeutralConId=" + str(order.m_deltaNeutralConId) \
              + " deltaNeutralSettlingFirm=" + str(order.m_deltaNeutralSettlingFirm) \
              + " deltaNeutralClearingAccount=" + str(order.m_deltaNeutralClearingAccount) \
              + " deltaNeutralClearingIntent=" + str(order.m_deltaNeutralClearingIntent) \
              + " deltaNeutralOpenClose=" + str(order.m_deltaNeutralOpenClose) \
              + " deltaNeutralShortSale=" + str(order.m_deltaNeutralShortSale) \
              + " deltaNeutralShortSaleSlot=" + str(order.m_deltaNeutralShortSaleSlot) \
              + " deltaNeutralDesignatedLocation=" + str(order.m_deltaNeutralDesignatedLocation) \
              + " continuousUpdate=" + str(order.m_continuousUpdate) \
              + " referencePriceType=" + str(order.m_referencePriceType) \
              + " trailStopPrice=" + Util.DoubleMaxString(order.m_trailStopPrice) \
              + " trailingPercent=" + Util.DoubleMaxString(order.m_trailingPercent) \
              + " scaleInitLevelSize=" + Util.IntMaxString(order.m_scaleInitLevelSize) \
              + " scaleSubsLevelSize=" + Util.IntMaxString(order.m_scaleSubsLevelSize) \
              + " scalePriceIncrement=" + Util.DoubleMaxString(order.m_scalePriceIncrement) \
              + " scalePriceAdjustValue=" + Util.DoubleMaxString(order.m_scalePriceAdjustValue) \
              + " scalePriceAdjustInterval=" + Util.IntMaxString(order.m_scalePriceAdjustInterval) \
              + " scaleProfitOffset=" + Util.DoubleMaxString(order.m_scaleProfitOffset) \
              + " scaleAutoReset=" + str(order.m_scaleAutoReset) \
              + " scaleInitPosition=" + Util.IntMaxString(order.m_scaleInitPosition) \
              + " scaleInitFillQty=" + Util.IntMaxString(order.m_scaleInitFillQty) \
              + " scaleRandomPercent=" + str(order.m_scaleRandomPercent) \
              + " hedgeType=" + str(order.m_hedgeType) \
              + " hedgeParam=" + str(order.m_hedgeParam) \
              + " account=" + str(order.m_account) \
              + " settlingFirm=" + str(order.m_settlingFirm) \
              + " clearingAccount=" + str(order.m_clearingAccount) \
              + " clearingIntent=" + str(order.m_clearingIntent) \
              + " notHeld=" + str(order.m_notHeld) \
              + " whatIf=" + str(order.m_whatIf)
        if "BAG" == contract.m_secType:
            if contract.m_comboLegsDescrip is not None:
                msg += " comboLegsDescrip=" + str(contract.m_comboLegsDescrip)
            msg += " comboLegs={"
            if contract.m_comboLegs is not None:
                i = 0
                while i < len(contract.m_comboLegs):
                    comboLeg = contract.m_comboLegs[i]
                    msg += " leg " + str(i + 1) + ": "
                    msg += "conId=" + str(comboLeg.m_conId)
                    msg += " ratio=" + str(comboLeg.m_ratio)
                    msg += " action=" + str(comboLeg.m_action)
                    msg += " exchange=" + str(comboLeg.m_exchange)
                    msg += " openClose=" + str(comboLeg.m_openClose)
                    msg += " shortSaleSlot=" + str(comboLeg.m_shortSaleSlot)
                    msg += " designatedLocation=" + str(comboLeg.m_designatedLocation)
                    msg += " exemptCode=" + str(comboLeg.m_exemptCode)
                    if order.m_orderComboLegs is not None and len(contract.m_comboLegs) == len(order.m_orderComboLegs):
                        orderComboLeg = order.m_orderComboLegs[i]
                        msg += " price=" + Util.DoubleMaxString(orderComboLeg.m_price)
                    msg += ";"
                    i += 1
            msg += "}"
            if order.m_basisPoints != Double.MAX_VALUE:
                msg += " basisPoints=" + Util.DoubleMaxString(order.m_basisPoints)
                msg += " basisPointsType=" + Util.IntMaxString(order.m_basisPointsType)
        if contract.m_underComp is not None:
            underComp = contract.m_underComp
            msg += " underComp.conId =" + str(underComp.m_conId) + " underComp.delta =" + str(underComp.m_delta) + " underComp.price =" + str(underComp.m_price)
        if not Util.StringIsEmpty(order.m_algoStrategy):
            msg += " algoStrategy=" + str(order.m_algoStrategy)
            msg += " algoParams={"
            if order.m_algoParams is not None:
                algoParams = order.m_algoParams
                i = 0
                while i < len(algoParams):
                    param = algoParams[i]
                    if i > 0:
                        msg += ","
                    msg += str(param.m_tag) + "=" + str(param.m_value)
                    i += 1
            msg += "}"
        if "BAG" == contract.m_secType:
            msg += " smartComboRoutingParams={"
            if order.m_smartComboRoutingParams is not None:
                smartComboRoutingParams = order.m_smartComboRoutingParams
                i = 0
                while i < len(smartComboRoutingParams):
                    param = smartComboRoutingParams[i]
                    if i > 0:
                        msg += ","
                    msg += str(param.m_tag) + "=" + str(param.m_value)
                    i += 1
            msg += "}"
        orderStateMsg = " status=" + str(orderState.m_status) \
                        + " initMargin=" + str(orderState.m_initMargin) \
                        + " maintMargin=" + str(orderState.m_maintMargin) \
                        + " equityWithLoan=" + str(orderState.m_equityWithLoan) \
                        + " commission=" + Util.DoubleMaxString(orderState.m_commission) \
                        + " minCommission=" + Util.DoubleMaxString(orderState.m_minCommission) \
                        + " maxCommission=" + Util.DoubleMaxString(orderState.m_maxCommission) \
                        + " commissionCurrency=" + str(orderState.m_commissionCurrency) \
                        + " warningText=" + str(orderState.m_warningText)
        return msg + orderStateMsg

    @classmethod
    def openOrderEnd(cls):
        """ generated source for method openOrderEnd """
        return " =============== end ==============="

    @classmethod
    def updateAccountValue(cls, key, value, currency, accountName):
        """ generated source for method updateAccountValue """
        return "updateAccountValue: " + key + " " + value + " " + currency + " " + accountName

    @classmethod
    def updatePortfolio(cls, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        """ generated source for method updatePortfolio """
        msg = "updatePortfolio: " + cls.contractMsg(contract) + \
              str(position) + " " + str(marketPrice) + " " + str(marketValue) + \
              " " + str(averageCost) + " " + str(unrealizedPNL) + " " + \
              str(realizedPNL) + " " + accountName
        return msg

    @classmethod
    def updateAccountTime(cls, timeStamp):
        """ generated source for method updateAccountTime """
        return "updateAccountTime: " + timeStamp

    @classmethod
    def accountDownloadEnd(cls, accountName):
        """ generated source for method accountDownloadEnd """
        return "accountDownloadEnd: " + accountName

    @classmethod
    def nextValidId(cls, orderId):
        """ generated source for method nextValidId """
        return "Next Valid Order ID: " + orderId

    @classmethod
    def contractDetails(cls, reqId, contractDetails):
        """ generated source for method contractDetails """
        contract = contractDetails.m_summary
        msg = "reqId = " + reqId + " ===================================\n" + \
              " ---- Contract Details begin ----\n" + \
              cls.contractMsg(contract) + cls.contractDetailsMsg(contractDetails) + \
              " ---- Contract Details End ----\n"
        return msg

    @classmethod
    def contractDetailsMsg(cls, contractDetails):
        """ generated source for method contractDetailsMsg """
        msg = "marketName = " + str(contractDetails.m_marketName) + "\n" \
              + "minTick = " + str(contractDetails.m_minTick) + "\n" \
              + "price magnifier = " + str(contractDetails.m_priceMagnifier) + "\n" \
              + "orderTypes = " + str(contractDetails.m_orderTypes) + "\n" \
              + "validExchanges = " + str(contractDetails.m_validExchanges) + "\n" \
              + "underConId = " + str(contractDetails.m_underConId) + "\n" \
              + "longName = " + str(contractDetails.m_longName) + "\n" \
              + "contractMonth = " + str(contractDetails.m_contractMonth) + "\n" \
              + "industry = " + str(contractDetails.m_industry) + "\n" \
              + "category = " + str(contractDetails.m_category) + "\n" \
              + "subcategory = " + str(contractDetails.m_subcategory) + "\n" \
              + "timeZoneId = " + str(contractDetails.m_timeZoneId) + "\n" \
              + "tradingHours = " + str(contractDetails.m_tradingHours) + "\n" \
              + "liquidHours = " + str(contractDetails.m_liquidHours) + "\n" \
              + "evRule = " + str(contractDetails.m_evRule) + "\n" \
              + "evMultiplier = " + str(contractDetails.m_evMultiplier) + "\n" \
              + cls.contractDetailsSecIdList(contractDetails)
        return msg

    @classmethod
    def contractMsg(cls, contract):
        """ generated source for method contractMsg """
        msg = "conid = " + str(contract.m_conId) + "\n" \
              + "symbol = " + str(contract.m_symbol) + "\n" \
              + "secType = " + str(contract.m_secType) + "\n" \
              + "expiry = " + str(contract.m_expiry) + "\n" \
              + "strike = " + str(contract.m_strike) + "\n" \
              + "right = " + str(contract.m_right) + "\n" \
              + "multiplier = " + str(contract.m_multiplier) + "\n" \
              + "exchange = " + str(contract.m_exchange) + "\n" \
              + "primaryExch = " + str(contract.m_primaryExch) + "\n" \
              + "currency = " + str(contract.m_currency) + "\n" \
              + "localSymbol = " + str(contract.m_localSymbol) + "\n" \
              + "tradingClass = " + str(contract.m_tradingClass) + "\n"
        return msg

    @classmethod
    def bondContractDetails(cls, reqId, contractDetails):
        """ generated source for method bondContractDetails """
        contract = contractDetails.m_summary
        msg = "reqId = " + str(reqId) + " ===================================\n" \
              + " ---- Bond Contract Details begin ----\n" \
              + "symbol = " + str(contract.m_symbol) + "\n" \
              + "secType = " + str(contract.m_secType) + "\n" \
              + "cusip = " + str(contractDetails.m_cusip) + "\n" \
              + "coupon = " + str(contractDetails.m_coupon) + "\n" \
              + "maturity = " + str(contractDetails.m_maturity) + "\n" \
              + "issueDate = " + str(contractDetails.m_issueDate) + "\n" \
              + "ratings = " + str(contractDetails.m_ratings) + "\n" \
              + "bondType = " + str(contractDetails.m_bondType) + "\n" \
              + "couponType = " + str(contractDetails.m_couponType) + "\n" \
              + "convertible = " + str(contractDetails.m_convertible) + "\n" \
              + "callable = " + str(contractDetails.m_callable) + "\n" \
              + "putable = " + str(contractDetails.m_putable) + "\n" \
              + "descAppend = " + str(contractDetails.m_descAppend) + "\n" \
              + "exchange = " + str(contract.m_exchange) + "\n" \
              + "currency = " + str(contract.m_currency) + "\n" \
              + "marketName = " + str(contractDetails.m_marketName) + "\n" \
              + "tradingClass = " + str(contract.m_tradingClass) + "\n" \
              + "conid = " + str(contract.m_conId) + "\n" \
              + "minTick = " + str(contractDetails.m_minTick) + "\n" \
              + "orderTypes = " + str(contractDetails.m_orderTypes) + "\n" \
              + "validExchanges = " + str(contractDetails.m_validExchanges) + "\n" \
              + "nextOptionDate = " + str(contractDetails.m_nextOptionDate) + "\n" \
              + "nextOptionType = " + str(contractDetails.m_nextOptionType) + "\n" \
              + "nextOptionPartial = " + str(contractDetails.m_nextOptionPartial) + "\n" \
              + "notes = " + str(contractDetails.m_notes) + "\n" \
              + "longName = " + str(contractDetails.m_longName) + "\n" \
              + "evRule = " + str(contractDetails.m_evRule) + "\n" \
              + "evMultiplier = " + str(contractDetails.m_evMultiplier) + "\n" \
              + cls.contractDetailsSecIdList(contractDetails) \
              + " ---- Bond Contract Details End ----\n"
        return msg

    @classmethod
    def contractDetailsSecIdList(cls, contractDetails):
        """ generated source for method contractDetailsSecIdList """
        msg = "secIdList={"
        if contractDetails.m_secIdList is not None:
            secIdList = contractDetails.m_secIdList
            i = 0
            while i < len(secIdList):
                param = secIdList[i]
                if i > 0:
                    msg += ","
                msg += str(param.m_tag) + "=" + str(param.m_value)
                i += 1
        msg += "}\n"
        return msg

    @classmethod
    def contractDetailsEnd(cls, reqId):
        """ generated source for method contractDetailsEnd """
        return "reqId = " + str(reqId) + " =============== end ==============="

    @classmethod
    def execDetails(cls, reqId, contract, execution):
        """ generated source for method execDetails """
        msg = " ---- Execution Details begin ----\n" \
              + "reqId = " + str(reqId) + "\n" \
              + "orderId = " + str(execution.m_orderId) + "\n" \
              + "clientId = " + str(execution.m_clientId) + "\n" \
              + cls.contractMsg(contract) \
              + "execId = " + str(execution.m_execId) + "\n" \
              + "time = " + str(execution.m_time) + "\n" \
              + "acctNumber = " + str(execution.m_acctNumber) + "\n" \
              + "executionExchange = " + str(execution.m_exchange) + "\n" \
              + "side = " + str(execution.m_side) + "\n" \
              + "shares = " + str(execution.m_shares) + "\n" \
              + "price = " + str(execution.m_price) + "\n" \
              + "permId = " + str(execution.m_permId) + "\n" \
              + "liquidation = " + str(execution.m_liquidation) + "\n" \
              + "cumQty = " + str(execution.m_cumQty) + "\n" \
              + "avgPrice = " + str(execution.m_avgPrice) + "\n" \
              + "orderRef = " + str(execution.m_orderRef) + "\n" \
              + "evRule = " + str(execution.m_evRule) + "\n" \
              + "evMultiplier = " + str(execution.m_evMultiplier) + "\n" \
              " ---- Execution Details end ----\n"
        return msg

    @classmethod
    def execDetailsEnd(cls, reqId):
        """ generated source for method execDetailsEnd """
        return "reqId = " + str(reqId) + " =============== end ==============="

    @classmethod
    def updateMktDepth(cls, tickerId, position, operation, side, price, size):
        """ generated source for method updateMktDepth """
        return "updateMktDepth: " + str(tickerId) + " " + str(position) + " " + str(operation) + " " + str(side) + " " + str(price) + " " + str(size)

    @classmethod
    def updateMktDepthL2(cls, tickerId, position, marketMaker, operation, side, price, size):
        """ generated source for method updateMktDepthL2 """
        return "updateMktDepth: " + str(tickerId) + " " + str(position) + " " + marketMaker + " " + str(operation) + " " + str(side) + " " + str(price) + " " + str(size)

    @classmethod
    def updateNewsBulletin(cls, msgId, msgType, message, origExchange):
        """ generated source for method updateNewsBulletin """
        return "MsgId=" + str(msgId) + " :: MsgType=" + str(msgType) + " :: Origin=" + origExchange + " :: Message=" + message

    @classmethod
    def managedAccounts(cls, accountsList):
        """ generated source for method managedAccounts """
        return "Connected : The list of managed accounts are : [" + accountsList + "]"

    @classmethod
    def receiveFA(cls, faDataType, xml):
        """ generated source for method receiveFA """
        return cls.FINANCIAL_ADVISOR + " " + EClientSocket.faMsgTypeName(faDataType) + " " + xml

    @classmethod
    def historicalData(cls, reqId, date, open, high, low, close, volume, count, WAP, hasGaps):
        """ generated source for method historicalData """
        return "id=" + str(reqId) \
               + " date = " + date \
               + " open=" + str(open) \
               + " high=" + str(high) \
               + " low=" + str(low) \
               + " close=" + str(close) \
               + " volume=" + str(volume) \
               + " count=" + str(count) \
               + " WAP=" + str(WAP) \
               + " hasGaps=" + str(hasGaps)

    @classmethod
    def realtimeBar(cls, reqId, time, open, high, low, close, volume, wap, count):
        """ generated source for method realtimeBar """
        return "id=" + str(reqId) \
               + " time = " + str(time) \
               + " open=" + str(open) \
               + " high=" + str(high) \
               + " low=" + str(low) \
               + " close=" + str(close) \
               + " volume=" + str(volume) \
               + " count=" + str(count) \
               + " WAP=" + str(wap)

    @classmethod
    def scannerParameters(cls, xml):
        """ generated source for method scannerParameters """
        return cls.SCANNER_PARAMETERS + "\n" + xml

    @classmethod
    def scannerData(cls, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        """ generated source for method scannerData """
        contract = contractDetails.m_summary
        return "id = " + str(reqId) \
               + " rank=" + str(rank) \
               + " symbol=" + str(contract.m_symbol) \
               + " secType=" + str(contract.m_secType) \
               + " expiry=" + str(contract.m_expiry) \
               + " strike=" + str(contract.m_strike) \
               + " right=" + str(contract.m_right) \
               + " exchange=" + str(contract.m_exchange) \
               + " currency=" + str(contract.m_currency) \
               + " localSymbol=" + str(contract.m_localSymbol) \
               + " marketName=" + str(contractDetails.m_marketName) \
               + " tradingClass=" + str(contract.m_tradingClass) \
               + " distance=" + distance \
               + " benchmark=" + benchmark \
               + " projection=" + projection \
               + " legsStr=" + legsStr

    @classmethod
    def scannerDataEnd(cls, reqId):
        """ generated source for method scannerDataEnd """
        return "id = " + str(reqId) + " =============== end ==============="

    @classmethod
    def currentTime(cls, time):
        """ generated source for method currentTime """
        return "current time = " + str(time)

    @classmethod
    def fundamentalData(cls, reqId, data):
        """ generated source for method fundamentalData """
        return "id  = " + str(reqId) + " len = " + str(len(data)) + '\n' + data

    @classmethod
    def deltaNeutralValidation(cls, reqId, underComp):
        """ generated source for method deltaNeutralValidation """
        return "id = " + str(reqId) + " underComp.conId =" + str(underComp.m_conId) + " underComp.delta =" + str(underComp.m_delta) + " underComp.price =" + str(underComp.m_price)

    @classmethod
    def tickSnapshotEnd(cls, tickerId):
        """ generated source for method tickSnapshotEnd """
        return "id=" + str(tickerId) + " =============== end ==============="

    @classmethod
    def marketDataType(cls, reqId, marketDataType):
        """ generated source for method marketDataType """
        return "id=" + str(reqId) + " marketDataType = " + MarketDataType.getField(marketDataType)

    @classmethod
    def commissionReport(cls, commissionReport):
        """ generated source for method commissionReport """
        msg = "commission report:" \
              + " execId=" + str(commissionReport.m_execId) \
              + " commission=" + Util.DoubleMaxString(commissionReport.m_commission) \
              + " currency=" + str(commissionReport.m_currency) \
              + " realizedPNL=" + Util.DoubleMaxString(commissionReport.m_realizedPNL) \
              + " yield=" + Util.DoubleMaxString(commissionReport.m_yield) \
              + " yieldRedemptionDate=" \
              + Util.IntMaxString(commissionReport.m_yieldRedemptionDate)
        return msg

    @classmethod
    def position(cls, account, contract, position, avgCost):
        """ generated source for method position """
        msg = " ---- Position begin ----\n" \
              + "account = " + str(account) + "\n" \
              + cls.contractMsg(contract) \
              + "position = " + Util.IntMaxString(position) + "\n" \
              + "avgCost = " + Util.DoubleMaxString(avgCost) + "\n" + \
              " ---- Position end ----\n"
        return msg

    @classmethod
    def positionEnd(cls):
        """ generated source for method positionEnd """
        return " =============== end ==============="

    @classmethod
    def accountSummary(cls, reqId, account, tag, value, currency):
        """ generated source for method accountSummary """
        msg = " ---- Account Summary begin ----\n" \
              + "reqId = " + str(reqId) + "\n" \
              + "account = " + str(account) + "\n" \
              + "tag = " + str(tag) + "\n" \
              + "value = " + str(value) + "\n" \
              + "currency = " + str(currency) + "\n" \
              + " ---- Account Summary end ----\n"
        return msg

    @classmethod
    def accountSummaryEnd(cls, reqId):
        """ generated source for method accountSummaryEnd """
        return "id=" + str(reqId) + " =============== end ==============="
