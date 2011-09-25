#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for EWrapperMsgGenerator.
##

# Source file: EWrapperMsgGenerator.java
# Target file: EWrapperMsgGenerator.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.ext.AnyWrapperMsgGenerator import AnyWrapperMsgGenerator
from ib.ext.Util import Util
from ib.ext.TickType import TickType
from ib.ext.EClientSocket import EClientSocket

class EWrapperMsgGenerator(AnyWrapperMsgGenerator):
    """ generated source for EWrapperMsgGenerator

    """
    SCANNER_PARAMETERS = "SCANNER PARAMETERS:"
    FINANCIAL_ADVISOR = "FA:"

    @classmethod
    def tickPrice(cls, tickerId, field, price, canAutoExecute):
        return "id=" + tickerId + "  " + TickType.getField(field) + "=" + price + " " + " canAutoExecute" if (canAutoExecute != 0) else " noAutoExecute"

    @classmethod
    def tickSize(cls, tickerId, field, size):
        return "id=" + tickerId + "  " + TickType.getField(field) + "=" + size

    @classmethod
    def tickOptionComputation(cls, tickerId,
                                   field,
                                   impliedVol,
                                   delta,
                                   optPrice,
                                   pvDividend,
                                   gamma,
                                   vega,
                                   theta,
                                   undPrice):
        toAdd = "id=" + tickerId + "  " + TickType.getField(field) + ": vol = " + (impliedVol if impliedVol >= 0 and (impliedVol != float('inf')) else "N/A") + " delta = " + (delta if abs(delta) <= 1 else "N/A") + " gamma = " + (gamma if abs(gamma) <= 1 else "N/A") + " vega = " + (vega if abs(vega) <= 1 else "N/A") + " theta = " + (theta if abs(theta) <= 1 else "N/A") + " optPrice = " + (optPrice if optPrice >= 0 and (optPrice != float('inf')) else "N/A") + " pvDividend = " + (pvDividend if pvDividend >= 0 and (pvDividend != float('inf')) else "N/A") + " undPrice = " + (undPrice if undPrice >= 0 and (undPrice != float('inf')) else "N/A")
        return toAdd

    @classmethod
    def tickGeneric(cls, tickerId, tickType, value):
        return "id=" + tickerId + "  " + TickType.getField(tickType) + "=" + value

    @classmethod
    def tickString(cls, tickerId, tickType, value):
        return "id=" + tickerId + "  " + TickType.getField(tickType) + "=" + value

    @classmethod
    def tickEFP(cls, tickerId,
                     tickType,
                     basisPoints,
                     formattedBasisPoints,
                     impliedFuture,
                     holdDays,
                     futureExpiry,
                     dividendImpact,
                     dividendsToExpiry):
        return "id=" + tickerId + "  " + TickType.getField(tickType) + ": basisPoints = " + basisPoints + "/" + formattedBasisPoints + " impliedFuture = " + impliedFuture + " holdDays = " + holdDays + " futureExpiry = " + futureExpiry + " dividendImpact = " + dividendImpact + " dividends to expiry = " + dividendsToExpiry

    @classmethod
    def orderStatus(cls, orderId,
                         status,
                         filled,
                         remaining,
                         avgFillPrice,
                         permId,
                         parentId,
                         lastFillPrice,
                         clientId,
                         whyHeld):
        return "order status: orderId=" + orderId + " clientId=" + clientId + " permId=" + permId + " status=" + status + " filled=" + filled + " remaining=" + remaining + " avgFillPrice=" + avgFillPrice + " lastFillPrice=" + lastFillPrice + " parent Id=" + parentId + " whyHeld=" + whyHeld

    @classmethod
    def openOrder(cls, orderId, contract, order, orderState):
        msg = "open order: orderId=" + orderId + " action=" + order.m_action + " quantity=" + order.m_totalQuantity + " symbol=" + contract.m_symbol + " exchange=" + contract.m_exchange + " secType=" + contract.m_secType + " type=" + order.m_orderType + " lmtPrice=" + order.m_lmtPrice + " auxPrice=" + order.m_auxPrice + " TIF=" + order.m_tif + " localSymbol=" + contract.m_localSymbol + " client Id=" + order.m_clientId + " parent Id=" + order.m_parentId + " permId=" + order.m_permId + " outsideRth=" + order.m_outsideRth + " hidden=" + order.m_hidden + " discretionaryAmt=" + order.m_discretionaryAmt + " triggerMethod=" + order.m_triggerMethod + " goodAfterTime=" + order.m_goodAfterTime + " goodTillDate=" + order.m_goodTillDate + " faGroup=" + order.m_faGroup + " faMethod=" + order.m_faMethod + " faPercentage=" + order.m_faPercentage + " faProfile=" + order.m_faProfile + " shortSaleSlot=" + order.m_shortSaleSlot + " designatedLocation=" + order.m_designatedLocation + " exemptCode=" + order.m_exemptCode + " ocaGroup=" + order.m_ocaGroup + " ocaType=" + order.m_ocaType + " rule80A=" + order.m_rule80A + " allOrNone=" + order.m_allOrNone + " minQty=" + order.m_minQty + " percentOffset=" + order.m_percentOffset + " eTradeOnly=" + order.m_eTradeOnly + " firmQuoteOnly=" + order.m_firmQuoteOnly + " nbboPriceCap=" + order.m_nbboPriceCap + " auctionStrategy=" + order.m_auctionStrategy + " startingPrice=" + order.m_startingPrice + " stockRefPrice=" + order.m_stockRefPrice + " delta=" + order.m_delta + " stockRangeLower=" + order.m_stockRangeLower + " stockRangeUpper=" + order.m_stockRangeUpper + " volatility=" + order.m_volatility + " volatilityType=" + order.m_volatilityType + " deltaNeutralOrderType=" + order.m_deltaNeutralOrderType + " deltaNeutralAuxPrice=" + order.m_deltaNeutralAuxPrice + " continuousUpdate=" + order.m_continuousUpdate + " referencePriceType=" + order.m_referencePriceType + " trailStopPrice=" + order.m_trailStopPrice + " scaleInitLevelSize=" + Util.IntMaxString(order.m_scaleInitLevelSize) + " scaleSubsLevelSize=" + Util.IntMaxString(order.m_scaleSubsLevelSize) + " scalePriceIncrement=" + Util.DoubleMaxString(order.m_scalePriceIncrement) + " account=" + order.m_account + " settlingFirm=" + order.m_settlingFirm + " clearingAccount=" + order.m_clearingAccount + " clearingIntent=" + order.m_clearingIntent + " notHeld=" + order.m_notHeld + " whatIf=" + order.m_whatIf
        if "BAG" == contract.m_secType:
            if contract.m_comboLegsDescrip is not None:
                msg += " comboLegsDescrip=" + contract.m_comboLegsDescrip
            if (order.m_basisPoints != float('inf')):
                msg += " basisPoints=" + order.m_basisPoints
                msg += " basisPointsType=" + order.m_basisPointsType
        if contract.m_underComp is not None:
            underComp = contract.m_underComp
            msg += " underComp.conId =" + underComp.m_conId + " underComp.delta =" + underComp.m_delta + " underComp.price =" + underComp.m_price
        if not Util.StringIsEmpty(order.m_algoStrategy):
            msg += " algoStrategy=" + order.m_algoStrategy
            msg += " algoParams={"
            if order.m_algoParams is not None:
                algoParams = order.m_algoParams
                ## for-while
                i = 0
                while i < len(algoParams):
                    param = algoParams.elementAt(i)
                    if i > 0:
                        msg += ","
                    msg += param.m_tag + "=" + param.m_value
                    i += 1
            msg += "}"
        orderStateMsg = " status=" + orderState.m_status + " initMargin=" + orderState.m_initMargin + " maintMargin=" + orderState.m_maintMargin + " equityWithLoan=" + orderState.m_equityWithLoan + " commission=" + Util.DoubleMaxString(orderState.m_commission) + " minCommission=" + Util.DoubleMaxString(orderState.m_minCommission) + " maxCommission=" + Util.DoubleMaxString(orderState.m_maxCommission) + " commissionCurrency=" + orderState.m_commissionCurrency + " warningText=" + orderState.m_warningText
        return msg + orderStateMsg

    @classmethod
    def openOrderEnd(cls):
        return " =============== end ==============="

    @classmethod
    def updateAccountValue(cls, key, value, currency, accountName):
        return "updateAccountValue: " + key + " " + value + " " + currency + " " + accountName

    @classmethod
    def updatePortfolio(cls, contract,
                             position,
                             marketPrice,
                             marketValue,
                             averageCost,
                             unrealizedPNL,
                             realizedPNL,
                             accountName):
        msg = "updatePortfolio: " + cls.contractMsg(contract) + position + " " + marketPrice + " " + marketValue + " " + averageCost + " " + unrealizedPNL + " " + realizedPNL + " " + accountName
        return msg

    @classmethod
    def updateAccountTime(cls, timeStamp):
        return "updateAccountTime: " + timeStamp

    @classmethod
    def accountDownloadEnd(cls, accountName):
        return "accountDownloadEnd: " + accountName

    @classmethod
    def nextValidId(cls, orderId):
        return "Next Valid Order ID: " + orderId

    @classmethod
    def contractDetails(cls, reqId, contractDetails):
        contract = cls.contractDetails.m_summary
        msg = "reqId = " + reqId + " ===================================\n" + " ---- Contract Details begin ----\n" + cls.contractMsg(contract) + cls.contractDetailsMsg(cls.contractDetails) + " ---- Contract Details End ----\n"
        return msg

    @classmethod
    def contractDetailsMsg(cls, contractDetails):
        msg = "marketName = " + cls.contractDetails.m_marketName + "\n" + "tradingClass = " + cls.contractDetails.m_tradingClass + "\n" + "minTick = " + cls.contractDetails.m_minTick + "\n" + "price magnifier = " + cls.contractDetails.m_priceMagnifier + "\n" + "orderTypes = " + cls.contractDetails.m_orderTypes + "\n" + "validExchanges = " + cls.contractDetails.m_validExchanges + "\n" + "underConId = " + cls.contractDetails.m_underConId + "\n" + "longName = " + cls.contractDetails.m_longName + "\n" + "contractMonth = " + cls.contractDetails.m_contractMonth + "\n" + "industry = " + cls.contractDetails.m_industry + "\n" + "category = " + cls.contractDetails.m_category + "\n" + "subcategory = " + cls.contractDetails.m_subcategory + "\n" + "timeZoneId = " + cls.contractDetails.m_timeZoneId + "\n" + "tradingHours = " + cls.contractDetails.m_tradingHours + "\n" + "liquidHours = " + cls.contractDetails.m_liquidHours + "\n"
        return msg

    @classmethod
    def contractMsg(cls, contract):
        msg = "conid = " + contract.m_conId + "\n" + "symbol = " + contract.m_symbol + "\n" + "secType = " + contract.m_secType + "\n" + "expiry = " + contract.m_expiry + "\n" + "strike = " + contract.m_strike + "\n" + "right = " + contract.m_right + "\n" + "multiplier = " + contract.m_multiplier + "\n" + "exchange = " + contract.m_exchange + "\n" + "primaryExch = " + contract.m_primaryExch + "\n" + "currency = " + contract.m_currency + "\n" + "localSymbol = " + contract.m_localSymbol + "\n"
        return msg

    @classmethod
    def bondContractDetails(cls, reqId, contractDetails):
        contract = cls.contractDetails.m_summary
        msg = "reqId = " + reqId + " ===================================\n" + " ---- Bond Contract Details begin ----\n" + "symbol = " + contract.m_symbol + "\n" + "secType = " + contract.m_secType + "\n" + "cusip = " + cls.contractDetails.m_cusip + "\n" + "coupon = " + cls.contractDetails.m_coupon + "\n" + "maturity = " + cls.contractDetails.m_maturity + "\n" + "issueDate = " + cls.contractDetails.m_issueDate + "\n" + "ratings = " + cls.contractDetails.m_ratings + "\n" + "bondType = " + cls.contractDetails.m_bondType + "\n" + "couponType = " + cls.contractDetails.m_couponType + "\n" + "convertible = " + cls.contractDetails.m_convertible + "\n" + "callable = " + cls.contractDetails.m_callable + "\n" + "putable = " + cls.contractDetails.m_putable + "\n" + "descAppend = " + cls.contractDetails.m_descAppend + "\n" + "exchange = " + contract.m_exchange + "\n" + "currency = " + contract.m_currency + "\n" + "marketName = " + cls.contractDetails.m_marketName + "\n" + "tradingClass = " + cls.contractDetails.m_tradingClass + "\n" + "conid = " + contract.m_conId + "\n" + "minTick = " + cls.contractDetails.m_minTick + "\n" + "orderTypes = " + cls.contractDetails.m_orderTypes + "\n" + "validExchanges = " + cls.contractDetails.m_validExchanges + "\n" + "nextOptionDate = " + cls.contractDetails.m_nextOptionDate + "\n" + "nextOptionType = " + cls.contractDetails.m_nextOptionType + "\n" + "nextOptionPartial = " + cls.contractDetails.m_nextOptionPartial + "\n" + "notes = " + cls.contractDetails.m_notes + "\n" + "longName = " + cls.contractDetails.m_longName + "\n" + " ---- Bond Contract Details End ----\n"
        return msg

    @classmethod
    def contractDetailsEnd(cls, reqId):
        return "reqId = " + reqId + " =============== end ==============="

    @classmethod
    def execDetails(cls, reqId, contract, execution):
        msg = " ---- Execution Details begin ----\n" + "reqId = " + reqId + "\n" + "orderId = " + execution.m_orderId + "\n" + "clientId = " + execution.m_clientId + "\n" + "symbol = " + contract.m_symbol + "\n" + "secType = " + contract.m_secType + "\n" + "expiry = " + contract.m_expiry + "\n" + "strike = " + contract.m_strike + "\n" + "right = " + contract.m_right + "\n" + "contractExchange = " + contract.m_exchange + "\n" + "currency = " + contract.m_currency + "\n" + "localSymbol = " + contract.m_localSymbol + "\n" + "execId = " + execution.m_execId + "\n" + "time = " + execution.m_time + "\n" + "acctNumber = " + execution.m_acctNumber + "\n" + "executionExchange = " + execution.m_exchange + "\n" + "side = " + execution.m_side + "\n" + "shares = " + execution.m_shares + "\n" + "price = " + execution.m_price + "\n" + "permId = " + execution.m_permId + "\n" + "liquidation = " + execution.m_liquidation + "\n" + "cumQty = " + execution.m_cumQty + "\n" + "avgPrice = " + execution.m_avgPrice + "\n" + " ---- Execution Details end ----\n"
        return msg

    @classmethod
    def execDetailsEnd(cls, reqId):
        return "reqId = " + reqId + " =============== end ==============="

    @classmethod
    def updateMktDepth(cls, tickerId,
                            position,
                            operation,
                            side,
                            price,
                            size):
        return "updateMktDepth: " + tickerId + " " + position + " " + operation + " " + side + " " + price + " " + size

    @classmethod
    def updateMktDepthL2(cls, tickerId,
                              position,
                              marketMaker,
                              operation,
                              side,
                              price,
                              size):
        return "updateMktDepth: " + tickerId + " " + position + " " + marketMaker + " " + operation + " " + side + " " + price + " " + size

    @classmethod
    def updateNewsBulletin(cls, msgId, msgType, message, origExchange):
        return "MsgId=" + msgId + " :: MsgType=" + msgType + " :: Origin=" + origExchange + " :: Message=" + message

    @classmethod
    def managedAccounts(cls, accountsList):
        return "Connected : The list of managed accounts are : [" + accountsList + "]"

    @classmethod
    def receiveFA(cls, faDataType, xml):
        return cls.FINANCIAL_ADVISOR + " " + EClientSocket.faMsgTypeName(faDataType) + " " + xml

    @classmethod
    def historicalData(cls, reqId,
                            date,
                            open,
                            high,
                            low,
                            close,
                            volume,
                            count,
                            WAP,
                            hasGaps):
        return "id=" + reqId + " date = " + date + " open=" + open + " high=" + high + " low=" + low + " close=" + close + " volume=" + volume + " count=" + count + " WAP=" + WAP + " hasGaps=" + hasGaps

    @classmethod
    def realtimeBar(cls, reqId,
                         time,
                         open,
                         high,
                         low,
                         close,
                         volume,
                         wap,
                         count):
        return "id=" + reqId + " time = " + time + " open=" + open + " high=" + high + " low=" + low + " close=" + close + " volume=" + volume + " count=" + count + " WAP=" + wap

    @classmethod
    def scannerParameters(cls, xml):
        return cls.SCANNER_PARAMETERS + "\n" + xml

    @classmethod
    def scannerData(cls, reqId,
                         rank,
                         contractDetails,
                         distance,
                         benchmark,
                         projection,
                         legsStr):
        contract = cls.contractDetails.m_summary
        return "id = " + reqId + " rank=" + rank + " symbol=" + contract.m_symbol + " secType=" + contract.m_secType + " expiry=" + contract.m_expiry + " strike=" + contract.m_strike + " right=" + contract.m_right + " exchange=" + contract.m_exchange + " currency=" + contract.m_currency + " localSymbol=" + contract.m_localSymbol + " marketName=" + cls.contractDetails.m_marketName + " tradingClass=" + cls.contractDetails.m_tradingClass + " distance=" + distance + " benchmark=" + benchmark + " projection=" + projection + " legsStr=" + legsStr

    @classmethod
    def scannerDataEnd(cls, reqId):
        return "id = " + reqId + " =============== end ==============="

    @classmethod
    def currentTime(cls, time):
        return "current time = " + time

    @classmethod
    def fundamentalData(cls, reqId, data):
        return "id  = " + reqId + " len = " + len(data) + '\n' + data

    @classmethod
    def deltaNeutralValidation(cls, reqId, underComp):
        return "id = " + reqId + " underComp.conId =" + underComp.m_conId + " underComp.delta =" + underComp.m_delta + " underComp.price =" + underComp.m_price

    @classmethod
    def tickSnapshotEnd(cls, tickerId):
        return "id=" + tickerId + " =============== end ==============="


