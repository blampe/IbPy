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
# WARNING: all changes made to this file will be lost.

from ib.ext.AnyWrapperMsgGenerator import AnyWrapperMsgGenerator

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
                                   modelPrice,
                                   pvDividend):
        toAdd = "id=" + tickerId + "  " + TickType.getField(field) + ": vol = " + Double.toString(impliedVol) if impliedVol >= 0 and (impliedVol != Double.MAX_VALUE) else "N/A" + " delta = " + Double.toString(delta) if Math.abs(delta) <= 1 else "N/A"
        if (field == TickType.MODEL_OPTION):
            toAdd += ": modelPrice = " + Double.toString(modelPrice) if modelPrice >= 0 and (modelPrice != Double.MAX_VALUE) else "N/A"
            toAdd += ": pvDividend = " + Double.toString(pvDividend) if pvDividend >= 0 and (pvDividend != Double.MAX_VALUE) else "N/A"
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
    def openOrder(cls, orderId, contract, order):
        msg = "open order: orderId=" + orderId + " action=" + order.m_action + " quantity=" + order.m_totalQuantity + " symbol=" + contract.m_symbol + " exchange=" + contract.m_exchange + " secType=" + contract.m_secType + " type=" + order.m_orderType + " lmtPrice=" + order.m_lmtPrice + " auxPrice=" + order.m_auxPrice + " TIF=" + order.m_tif + " localSymbol=" + contract.m_localSymbol + " client Id=" + order.m_clientId + " parent Id=" + order.m_parentId + " permId=" + order.m_permId + " ignoreRth=" + order.m_ignoreRth + " hidden=" + order.m_hidden + " discretionaryAmt=" + order.m_discretionaryAmt + " triggerMethod=" + order.m_triggerMethod + " goodAfterTime=" + order.m_goodAfterTime + " goodTillDate=" + order.m_goodTillDate + " account=" + order.m_account + " allocation=" + order.m_sharesAllocation + " faGroup=" + order.m_faGroup + " faMethod=" + order.m_faMethod + " faPercentage=" + order.m_faPercentage + " faProfile=" + order.m_faProfile + " shortSaleSlot=" + order.m_shortSaleSlot + " designatedLocation=" + order.m_designatedLocation + " ocaGroup=" + order.m_ocaGroup + " ocaType=" + order.m_ocaType + " rthOnly=" + order.m_rthOnly + " rule80A=" + order.m_rule80A + " settlingFirm=" + order.m_settlingFirm + " allOrNone=" + order.m_allOrNone + " minQty=" + order.m_minQty + " percentOffset=" + order.m_percentOffset + " eTradeOnly=" + order.m_eTradeOnly + " firmQuoteOnly=" + order.m_firmQuoteOnly + " nbboPriceCap=" + order.m_nbboPriceCap + " auctionStrategy=" + order.m_auctionStrategy + " startingPrice=" + order.m_startingPrice + " stockRefPrice=" + order.m_stockRefPrice + " delta=" + order.m_delta + " stockRangeLower=" + order.m_stockRangeLower + " stockRangeUpper=" + order.m_stockRangeUpper + " volatility=" + order.m_volatility + " volatilityType=" + order.m_volatilityType + " deltaNeutralOrderType=" + order.m_deltaNeutralOrderType + " deltaNeutralAuxPrice=" + order.m_deltaNeutralAuxPrice + " continuousUpdate=" + order.m_continuousUpdate + " referencePriceType=" + order.m_referencePriceType + " trailStopPrice=" + order.m_trailStopPrice
        if "BAG" == contract.m_secType:
            if contract.m_comboLegsDescrip is not None:
                msg += " comboLegsDescrip=" + contract.m_comboLegsDescrip
            if (order.m_basisPoints != Double.MAX_VALUE):
                msg += " basisPoints=" + order.m_basisPoints
                msg += " basisPointsType=" + order.m_basisPointsType
        return msg

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
    def nextValidId(cls, orderId):
        return "Next Valid Order ID: " + orderId

    @classmethod
    def contractDetails(cls, contractDetails):
        contract = cls.contractDetails.m_summary
        msg = " ---- Contract Details begin ----\n" + cls.contractMsg(contract) + cls.contractDetailsMsg(cls.contractDetails) + " ---- Contract Details End ----\n"
        return msg

    @classmethod
    def contractDetailsMsg(cls, contractDetails):
        msg = "marketName = " + cls.contractDetails.m_marketName + "\n" + "tradingClass = " + cls.contractDetails.m_tradingClass + "\n" + "conid = " + cls.contractDetails.m_conid + "\n" + "minTick = " + cls.contractDetails.m_minTick + "\n" + "multiplier = " + cls.contractDetails.m_multiplier + "\n" + "price magnifier = " + cls.contractDetails.m_priceMagnifier + "\n" + "orderTypes = " + cls.contractDetails.m_orderTypes + "\n" + "validExchanges = " + cls.contractDetails.m_validExchanges + "\n"
        return msg

    @classmethod
    def contractMsg(cls, contract):
        msg = " ---- Contract Details begin ----\n" + "symbol = " + contract.m_symbol + "\n" + "secType = " + contract.m_secType + "\n" + "expiry = " + contract.m_expiry + "\n" + "strike = " + contract.m_strike + "\n" + "right = " + contract.m_right + "\n" + "exchange = " + contract.m_exchange + "\n" + "currency = " + contract.m_currency + "\n" + "localSymbol = " + contract.m_localSymbol + "\n"
        return msg

    @classmethod
    def bondContractDetails(cls, contractDetails):
        contract = cls.contractDetails.m_summary
        msg = " ---- Bond Contract Details begin ----\n" + "symbol = " + contract.m_symbol + "\n" + "secType = " + contract.m_secType + "\n" + "cusip = " + contract.m_cusip + "\n" + "coupon = " + contract.m_coupon + "\n" + "maturity = " + contract.m_maturity + "\n" + "issueDate = " + contract.m_issueDate + "\n" + "ratings = " + contract.m_ratings + "\n" + "bondType = " + contract.m_bondType + "\n" + "couponType = " + contract.m_couponType + "\n" + "convertible = " + contract.m_convertible + "\n" + "callable = " + contract.m_callable + "\n" + "putable = " + contract.m_putable + "\n" + "descAppend = " + contract.m_descAppend + "\n" + "exchange = " + contract.m_exchange + "\n" + "currency = " + contract.m_currency + "\n" + "marketName = " + cls.contractDetails.m_marketName + "\n" + "tradingClass = " + cls.contractDetails.m_tradingClass + "\n" + "conid = " + cls.contractDetails.m_conid + "\n" + "minTick = " + cls.contractDetails.m_minTick + "\n" + "orderTypes = " + cls.contractDetails.m_orderTypes + "\n" + "validExchanges = " + cls.contractDetails.m_validExchanges + "\n" + "nextOptionDate = " + contract.m_nextOptionDate + "\n" + "nextOptionType = " + contract.m_nextOptionType + "\n" + "nextOptionPartial = " + contract.m_nextOptionPartial + "\n" + "notes = " + contract.m_notes + "\n" + " ---- Bond Contract Details End ----\n"
        return msg

    @classmethod
    def execDetails(cls, orderId, contract, execution):
        msg = " ---- Execution Details begin ----\n" + "orderId = " + str(orderId) + "\n" + "clientId = " + str(execution.m_clientId) + "\n" + "symbol = " + contract.m_symbol + "\n" + "secType = " + contract.m_secType + "\n" + "expiry = " + contract.m_expiry + "\n" + "strike = " + contract.m_strike + "\n" + "right = " + contract.m_right + "\n" + "contractExchange = " + contract.m_exchange + "\n" + "currency = " + contract.m_currency + "\n" + "localSymbol = " + contract.m_localSymbol + "\n" + "execId = " + execution.m_execId + "\n" + "time = " + execution.m_time + "\n" + "acctNumber = " + execution.m_acctNumber + "\n" + "executionExchange = " + execution.m_exchange + "\n" + "side = " + execution.m_side + "\n" + "shares = " + execution.m_shares + "\n" + "price = " + execution.m_price + "\n" + "permId = " + execution.m_permId + "\n" + "liquidation = " + execution.m_liquidation + "\n" + " ---- Execution Details end ----\n"
        return msg

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
    def currentTime(cls, time):
        return "current time = " + time + " (" + DateFormat.getDateTimeInstance().format(Date(time * 1000)) + ")"


