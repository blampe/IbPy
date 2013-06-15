#!/usr/bin/env python
""" generated source for module EWrapper """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.
from abc import ABCMeta, abstractmethod

from ib.ext.AnyWrapper import AnyWrapper
# 
#  * EWrapper.java
#  *
#  
# package: com.ib.client
class EWrapper(AnyWrapper):
    """ generated source for interface EWrapper """
    __metaclass__ = ABCMeta
    # /////////////////////////////////////////////////////////////////////
    #  Interface methods
    # /////////////////////////////////////////////////////////////////////
    @abstractmethod
    def tickPrice(self, tickerId, field, price, canAutoExecute):
        """ generated source for method tickPrice """

    @abstractmethod
    def tickSize(self, tickerId, field, size):
        """ generated source for method tickSize """

    @abstractmethod
    def tickOptionComputation(self, tickerId, field, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        """ generated source for method tickOptionComputation """

    @abstractmethod
    def tickGeneric(self, tickerId, tickType, value):
        """ generated source for method tickGeneric """

    @abstractmethod
    def tickString(self, tickerId, tickType, value):
        """ generated source for method tickString """

    @abstractmethod
    def tickEFP(self, tickerId, tickType, basisPoints, formattedBasisPoints, impliedFuture, holdDays, futureExpiry, dividendImpact, dividendsToExpiry):
        """ generated source for method tickEFP """

    @abstractmethod
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld):
        """ generated source for method orderStatus """

    @abstractmethod
    def openOrder(self, orderId, contract, order, orderState):
        """ generated source for method openOrder """

    @abstractmethod
    def openOrderEnd(self):
        """ generated source for method openOrderEnd """

    @abstractmethod
    def updateAccountValue(self, key, value, currency, accountName):
        """ generated source for method updateAccountValue """

    @abstractmethod
    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        """ generated source for method updatePortfolio """

    @abstractmethod
    def updateAccountTime(self, timeStamp):
        """ generated source for method updateAccountTime """

    @abstractmethod
    def accountDownloadEnd(self, accountName):
        """ generated source for method accountDownloadEnd """

    @abstractmethod
    def nextValidId(self, orderId):
        """ generated source for method nextValidId """

    @abstractmethod
    def contractDetails(self, reqId, contractDetails):
        """ generated source for method contractDetails """

    @abstractmethod
    def bondContractDetails(self, reqId, contractDetails):
        """ generated source for method bondContractDetails """

    @abstractmethod
    def contractDetailsEnd(self, reqId):
        """ generated source for method contractDetailsEnd """

    @abstractmethod
    def execDetails(self, reqId, contract, execution):
        """ generated source for method execDetails """

    @abstractmethod
    def execDetailsEnd(self, reqId):
        """ generated source for method execDetailsEnd """

    @abstractmethod
    def updateMktDepth(self, tickerId, position, operation, side, price, size):
        """ generated source for method updateMktDepth """

    @abstractmethod
    def updateMktDepthL2(self, tickerId, position, marketMaker, operation, side, price, size):
        """ generated source for method updateMktDepthL2 """

    @abstractmethod
    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        """ generated source for method updateNewsBulletin """

    @abstractmethod
    def managedAccounts(self, accountsList):
        """ generated source for method managedAccounts """

    @abstractmethod
    def receiveFA(self, faDataType, xml):
        """ generated source for method receiveFA """

    @abstractmethod
    def historicalData(self, reqId, date, open, high, low, close, volume, count, WAP, hasGaps):
        """ generated source for method historicalData """

    @abstractmethod
    def scannerParameters(self, xml):
        """ generated source for method scannerParameters """

    @abstractmethod
    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        """ generated source for method scannerData """

    @abstractmethod
    def scannerDataEnd(self, reqId):
        """ generated source for method scannerDataEnd """

    @abstractmethod
    def realtimeBar(self, reqId, time, open, high, low, close, volume, wap, count):
        """ generated source for method realtimeBar """

    @abstractmethod
    def currentTime(self, time):
        """ generated source for method currentTime """

    @abstractmethod
    def fundamentalData(self, reqId, data):
        """ generated source for method fundamentalData """

    @abstractmethod
    def deltaNeutralValidation(self, reqId, underComp):
        """ generated source for method deltaNeutralValidation """

    @abstractmethod
    def tickSnapshotEnd(self, reqId):
        """ generated source for method tickSnapshotEnd """

    @abstractmethod
    def marketDataType(self, reqId, marketDataType):
        """ generated source for method marketDataType """

    @abstractmethod
    def commissionReport(self, commissionReport):
        """ generated source for method commissionReport """

