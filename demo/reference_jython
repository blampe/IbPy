#!/usr/bin/env jython
""" ib.demo.reference -> jython script to exercise the entire TWS API
via its Java code.

This could be written in Java, but then it would be written in Java.

"""
import sys
import time

try:
    import java
except (ImportError, ):
    print 'Run this script with jython, not python.'
    sys.exit(1)
try:
    import com.ib
except (ImportError, ):
    print 'Could not import com.ib.  Try adding jtsclient.jar to CLASSPATH.'
    sys.exit(2)
import com.ib.client


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


class ReferenceWrapper(com.ib.client.EWrapper):
    def tickPrice(self, tickerId, field, price, canAutoExecute):
        showmessage('tickPrice', vars())

    def tickSize(self, tickerId, field, size):
        showmessage('tickSize', vars())

    def tickOptionComputation(self, tickerId, field, impliedVolatility, delta):
        showmessage('tickOptionComputation', vars())

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId):
        showmessage('orderStatus', vars())

    def openOrder(self, orderId, contract, order):
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

    def historicalData(self, reqId, date, open, high, low, close, volume, WAP, hasGaps):
        showmessage('historicalData', vars())

    def scannerParameters(self, xml):
        showmessage('scannerParameters', vars())

    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection):
        showmessage('scannerData', vars())


class ReferenceApp:
    def __init__(self, host='localhost', port=7496, clientId=0):
        self.host = host
        self.port = port
        self.clientId = clientId
        self.wrapper = ReferenceWrapper()
        self.reader = com.ib.client.EClientSocket(self.wrapper)

    def eConnect(self):
        self.reader.eConnect(self.host, self.port, self.clientId)

    def reqAccountUpdates(self):
        self.reader.reqAccountUpdates(1, '')

    def reqOpenOrders(self):
        self.reader.reqOpenOrders()

    def reqExecutions(self):
        filt = com.ib.client.ExecutionFilter()
        self.reader.reqExecutions(filt)

    def reqIds(self):
        self.reader.reqIds(10)

    def reqNewsBulletins(self):
        self.reader.reqNewsBulletins(1)

    def cancelNewsBulletins(self):
        self.reader.cancelNewsBulletins()

    def setServerLogLevel(self):
        self.reader.setServerLogLevel(3)

    def reqAutoOpenOrders(self):
        self.reader.reqAutoOpenOrders(1)

    def reqAllOpenOrders(self):
        self.reader.reqAllOpenOrders()

    def reqManagedAccts(self):
        self.reader.reqManagedAccts()

    def requestFA(self):
        self.reader.requestFA(1)

    def reqMktData(self):
        contract = com.ib.client.Contract() #
        contract.m_symbol = 'QQQQ'
        contract.m_secType = 'STK'
        contract.m_exchange = 'SMART'
        self.reader.reqMktData(1, contract, '', False)

    def reqHistoricalData(self):
        contract = com.ib.client.Contract()
        contract.m_symbol = 'QQQQ'
        contract.m_secType = 'STK'
        contract.m_exchange = 'SMART'
        self.reader.reqHistoricalData(1,
                                      contract,
                                      "20070118 05:00:00 GMT",
                                      "300 S",
                                      1, # 1-11
                                      "MIDPOINT",
                                      1, # rth - regular trading hours
                                      1) # date style - 1 or 2

    def eDisconnect(self):
        time.sleep(5)
        self.reader.eDisconnect()


if __name__ == '__main__':
    app = ReferenceApp()
    args = sys.argv[1:]

    if not args:
        args = ['eConnect', 'eDisconnect', ]
    else:
        if 'eConnect' not in args:
            args.insert(0, 'eConnect')
        if 'eDisconnect' not in args:
            args.append('eDisconnect')

    print '### calling functions:', args
    for name in args:
        call = getattr(app, name, None)
        if call is None:
            print '### warning: no call %s' % (name, )
        call()



['ComboLeg', 'Contract', 'ContractDetails', 'EClientErrors',
 'EClientSocket', 'EWrapper', 'Execution', 'ExecutionFilter', 'Order',
 'ScannerSubscription', 'TickType', '__name__']
