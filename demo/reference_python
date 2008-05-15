#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# This script is an exmple of using the generated code within IbPy in
# the same manner as the Java code.  We subclass EWrapper and give an
# instance of the wrapper to an EClientSocket.
##

from sys import argv
from time import sleep, strftime

from ib.ext.Contract import Contract
from ib.ext.EWrapper import EWrapper
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ExecutionFilter import ExecutionFilter


def showmessage(message, mapping):
    try:
        del(mapping['self'])
    except (KeyError, ):
        pass
    items = mapping.items()
    items.sort()
    print '### %s' % (message, )
    for k, v in items:
        print '    %s:%s' % (k, v)


class ReferenceWrapper(EWrapper):
    def tickPrice(self, tickerId, field, price, canAutoExecute):
        showmessage('tickPrice', vars())

    def tickSize(self, tickerId, field, size):
        showmessage('tickSize', vars())

    def tickString(self, tickerId, tickType, value):
        showmessage('tickString', vars())

    def tickOptionComputation(self, tickerId, field, impliedVolatility, delta):
        showmessage('tickOptionComputation', vars())

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeId):
        showmessage('orderStatus', vars())

    def openOrder(self, orderId, contract, order, state):
        showmessage('openOrder', vars())

    def connectionClosed(self):
        showmessage('connectionClosed', {})

    def updateAccountValue(self, key, value, currency, accountName):
        showmessage('updateAccountValue', vars())

    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        showmessage('updatePortfolio', vars())

    def updateAccountTime(self, timeStamp):
        showmessage('updateAccountTime', vars())

    def nextValidId(self, orderId):
        showmessage('nextValidId', vars())

    def contractDetails(self, contractDetails):
        showmessage('contractDetails', vars())

    def bondContractDetails(self, contractDetails):
        showmessage('bondContractDetails', vars())

    def execDetails(self, orderId, contract, execution):
        showmessage('execDetails', vars())

    def error(self, id=None, errorCode=None, errorMsg=None):
        showmessage('error', vars())

    def updateMktDepth(self, tickerId, position, operation, side, price, size):
        showmessage('updateMktDepth', vars())

    def updateMktDepthL2(self, tickerId, position, marketMaker, operation, side, price, size):
        showmessage('updateMktDepthL2', vars())

    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        showmessage('updateNewsBulletin', vars())

    def managedAccounts(self, accountsList):
        showmessage('managedAccounts', vars())

    def receiveFA(self, faDataType, xml):
        showmessage('receiveFA', vars())

    def historicalData(self, reqId, date, open, high, low, close, volume, count, WAP, hasGaps):
        showmessage('historicalData', vars())

    def scannerParameters(self, xml):
        showmessage('scannerParameters', vars())

    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection):
        showmessage('scannerData', vars())


allMethods = []
def ref(method):
    allMethods.append(method.__name__)
    return method


class ReferenceApp:
    def __init__(self, host='localhost', port=7496, clientId=0):
        self.host = host
        self.port = port
        self.clientId = clientId
        self.wrapper = ReferenceWrapper()
        self.connection = EClientSocket(self.wrapper)

    @ref
    def eConnect(self):
        self.connection.eConnect(self.host, self.port, self.clientId)

    @ref
    def reqAccountUpdates(self):
        self.connection.reqAccountUpdates(1, '')

    @ref
    def reqOpenOrders(self):
        self.connection.reqOpenOrders()

    @ref
    def reqExecutions(self):
        filt = ExecutionFilter()
        self.connection.reqExecutions(filt)

    @ref
    def reqIds(self):
        self.connection.reqIds(10)

    @ref
    def reqNewsBulletins(self):
        self.connection.reqNewsBulletins(1)

    @ref
    def cancelNewsBulletins(self):
        self.connection.cancelNewsBulletins()

    @ref
    def setServerLogLevel(self):
        self.connection.setServerLogLevel(3)

    @ref
    def reqAutoOpenOrders(self):
        self.connection.reqAutoOpenOrders(1)

    @ref
    def reqAllOpenOrders(self):
        self.connection.reqAllOpenOrders()

    @ref
    def reqManagedAccts(self):
        self.connection.reqManagedAccts()

    @ref
    def requestFA(self):
        self.connection.requestFA(1)

    @ref
    def reqMktData(self):
        contract = Contract() #
        contract.m_symbol = 'QQQQ'
        contract.m_secType = 'STK'
        contract.m_exchange = 'SMART'
        self.connection.reqMktData(1, contract, '', False)

    @ref
    def reqHistoricalData(self):
        contract = Contract()
        contract.m_symbol = 'QQQQ'
        contract.m_secType = 'STK'
        contract.m_exchange = 'SMART'
        endtime = strftime('%Y%m%d %H:%M:%S')
        self.connection.reqHistoricalData(
            tickerId=1,
            contract=contract,
            endDateTime=endtime,
            durationStr='1 D',
            barSizeSetting='1 min',
            whatToShow='TRADES',
            useRTH=0,
            formatDate=1)

    @ref
    def eDisconnect(self):
        sleep(5)
        self.connection.eDisconnect()


if __name__ == '__main__':
    app = ReferenceApp()
    methods = argv[1:]

    if not methods:
        methods = ['eConnect', 'eDisconnect', ]
    elif methods == ['all']:
        methods = allMethods
    if 'eConnect' not in methods:
        methods.insert(0, 'eConnect')
    if 'eDisconnect' not in methods:
        methods.append('eDisconnect')

    print '### calling functions:', str.join(', ', methods)
    for mname in methods:
        call = getattr(app, mname, None)
        if call is None:
            print '### warning: no call %s' % (mname, )
        else:
            print '## calling', call.im_func.func_name
            call()
            print '## called', call.im_func.func_name

