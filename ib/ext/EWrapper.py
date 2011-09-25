#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for EWrapper.
##

# Source file: EWrapper.java
# Target file: EWrapper.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.ext.AnyWrapper import AnyWrapper

class EWrapper(AnyWrapper):
    """ generated source for EWrapper

    """

    def tickPrice(self, tickerId, field, price, canAutoExecute):
        raise NotImplementedError()

    def tickSize(self, tickerId, field, size):
        raise NotImplementedError()

    def tickOptionComputation(self, tickerId,
                                    field,
                                    impliedVol,
                                    delta,
                                    optPrice,
                                    pvDividend,
                                    gamma,
                                    vega,
                                    theta,
                                    undPrice):
        raise NotImplementedError()

    def tickGeneric(self, tickerId, tickType, value):
        raise NotImplementedError()

    def tickString(self, tickerId, tickType, value):
        raise NotImplementedError()

    def tickEFP(self, tickerId,
                      tickType,
                      basisPoints,
                      formattedBasisPoints,
                      impliedFuture,
                      holdDays,
                      futureExpiry,
                      dividendImpact,
                      dividendsToExpiry):
        raise NotImplementedError()

    def orderStatus(self, orderId,
                          status,
                          filled,
                          remaining,
                          avgFillPrice,
                          permId,
                          parentId,
                          lastFillPrice,
                          clientId,
                          whyHeld):
        raise NotImplementedError()

    def openOrder(self, orderId, contract, order, orderState):
        raise NotImplementedError()

    def openOrderEnd(self):
        raise NotImplementedError()

    def updateAccountValue(self, key, value, currency, accountName):
        raise NotImplementedError()

    def updatePortfolio(self, contract,
                              position,
                              marketPrice,
                              marketValue,
                              averageCost,
                              unrealizedPNL,
                              realizedPNL,
                              accountName):
        raise NotImplementedError()

    def updateAccountTime(self, timeStamp):
        raise NotImplementedError()

    def accountDownloadEnd(self, accountName):
        raise NotImplementedError()

    def nextValidId(self, orderId):
        raise NotImplementedError()

    def contractDetails(self, reqId, contractDetails):
        raise NotImplementedError()

    def bondContractDetails(self, reqId, contractDetails):
        raise NotImplementedError()

    def contractDetailsEnd(self, reqId):
        raise NotImplementedError()

    def execDetails(self, reqId, contract, execution):
        raise NotImplementedError()

    def execDetailsEnd(self, reqId):
        raise NotImplementedError()

    def updateMktDepth(self, tickerId,
                             position,
                             operation,
                             side,
                             price,
                             size):
        raise NotImplementedError()

    def updateMktDepthL2(self, tickerId,
                               position,
                               marketMaker,
                               operation,
                               side,
                               price,
                               size):
        raise NotImplementedError()

    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        raise NotImplementedError()

    def managedAccounts(self, accountsList):
        raise NotImplementedError()

    def receiveFA(self, faDataType, xml):
        raise NotImplementedError()

    def historicalData(self, reqId,
                             date,
                             open,
                             high,
                             low,
                             close,
                             volume,
                             count,
                             WAP,
                             hasGaps):
        raise NotImplementedError()

    def scannerParameters(self, xml):
        raise NotImplementedError()

    def scannerData(self, reqId,
                          rank,
                          contractDetails,
                          distance,
                          benchmark,
                          projection,
                          legsStr):
        raise NotImplementedError()

    def scannerDataEnd(self, reqId):
        raise NotImplementedError()

    def realtimeBar(self, reqId,
                          time,
                          open,
                          high,
                          low,
                          close,
                          volume,
                          wap,
                          count):
        raise NotImplementedError()

    def currentTime(self, time):
        raise NotImplementedError()

    def fundamentalData(self, reqId, data):
        raise NotImplementedError()

    def deltaNeutralValidation(self, reqId, underComp):
        raise NotImplementedError()

    def tickSnapshotEnd(self, reqId):
        raise NotImplementedError()


