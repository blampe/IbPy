#!/usr/bin/env python
""" ib.demo.simple -> a module not unlike a demo, a module not unlike a unittest

The SimpleMessageHandler and AutomaticDemoApp classes show a
simplistic way of constructing an application that uses ibpy.  The
AutomaticDemoApp class makes a connection, a SimpleMessageHandler, and
makes the association between the two.
"""
import os
import sys
import time

import ib.types
import ib.client
import ib.client.message


class SimpleMessageHandler:
    """ SimpleMessageHandler() -> defines methods suitable for IbPy callbacks

    """
    orderId = 0    
    outstream = sys.stdout


    def onConnect(self, msg):
        """ onConnect(msg) -> executed when IbPy connects to TWS

        """
        print >> self.outstream, 'connected', msg


    def onDisconnect(self, msg):
        """ onDisconnect(msg) -> executed when IbPy disconnects from TWS

        """
        print >> self.outstream, 'disconnected', msg


    def onAccountUpdate(self, msg):
        """ onAccountUpdate(msg) -> called when account values change

        """
        print >> self.outstream, 'Account value changed: %s is %s' % (msg.key, msg.value, )


    def onError(self, msg):
        """ onError(msg) -> called when TWS reports an error

        """
        err = (msg.error_id, msg.error_code, msg.error_msg, )
        print >> self.outstream, 'An Error from TWS: %s %s %s' % err


    def onTickerUpdate(self, msg):
        """ onTickerUpdate(msg) -> called when ticker price or size data has changed

        """
        print >> self.outstream, msg


    def onNextOrderId(self, msg):
        """ onNextOrderId(msg) -> called to tell us the first usable order id

        """
        self.orderId = msg.nextValidId
        print >> self.outstream, msg


    def onOrderStatus(self, msg):
        """ onOrderStatus(msg) -> called when order status has changed

        """
        ordinfo = (msg.orderId, msg.message, )
        print >> self.outstream, 'Order status changed:  order id %s, status %s' % ordinfo


    def onOpenOrder(self, msg):
        """ onOpenOrder(msg) -> called for every existing order

        """


    def onContractDetails(self, msg):
        """ onContractDetails(msg) -> called with details on a contract

        """
        print >> self.outstream, msg


    def onManagedAccounts(self, msg):
        """ onManagedAccounts(msg) -> called with a list of accounts manage

        """


    def onNewsBulletin(self, msg):
        """ onNewsBulletin(msg) -> called when there is news!

        """


    def onExecutionDetails(self, msg):
        """ onExecutionDetails(msg) -> called with execution details

        """


    def onPortfolioUpdate(self, msg):
        """ onPortfolioUpdate(msg) -> called when the portfolio has changed

        """


    def onHistoricalData(self, msg):
        print >> self.outstream, msg


class AutomaticDemoApp:
    """ AutomaticDemoApp() -> something not unlike a demonstration.

    """
    snooze = 3
    serverLogLevel = 3
    tickers = dict(DELL=4000, AAPL=4001, INTC=4002)


    def __init__(self, dsn=('localhost', 7496)):

        ## first thing we do is create a new connection object
        self.connection = ib.client.build(next_connection_id())

        ## next we create something to handle the messages read from
        ## the connection.  this could be more than one class, a
        ## collection of functions, thread methods, etc.  in this
        ## example we're using a single class instance to process all
        ## of the incoming messages.
        self.handler = handler = SimpleMessageHandler()

        ## here we associate the connection with our handler instance.
        ## again, these could be multiple functions, instance methods,
        ## or any other callable types instead.
        register = self.connection.register
        message = ib.client.message

        register(message.ContractDetails, handler.onContractDetails)
        register(message.Error, handler.onError)
        register(message.Execution, handler.onExecutionDetails)
        register(message.ManagedAccounts, handler.onManagedAccounts)
        register(message.NextId, handler.onNextOrderId)
        register(message.NewsBulletin, handler.onNewsBulletin)
        register(message.OpenOrder, handler.onOpenOrder)
        register(message.OrderStatus, handler.onOrderStatus)
        register(message.Portfolio, handler.onPortfolioUpdate)
        register(message.ReaderStart, handler.onConnect)
        register(message.ReaderStop, handler.onDisconnect)
        register(message.HistoricalData, handler.onHistoricalData)

        ## there is more than one type of account update message, and
        ## more than one type of ticker message.  here we associate
        ## all types with their respective handlers by refering to the
        ## generated message's base class.
        register(message.AccountBase, handler.onAccountUpdate)
        register(message.TickBase, handler.onTickerUpdate)

        ## now that the connection is associated with our callables,
        ## we can connect the connection object to tws.
        self.connection.connect(dsn)

        ## and because we're automatic, we can go ahead and run all of
        ## instance methods on this class that start with 'demo'.
        funcs = [getattr(self, n) for n in dir(self) if n.startswith('demo')]
        funcs.sort()
        for func in funcs:
            func()


    def demo000_MakeRequests(self):
        """ make requests for account data, ticker data, etc.

        """
        connection = self.connection
        connection.setServerLogLevel(self.serverLogLevel)
        connection.reqAccountUpdates()
        connection.reqOpenOrders()
        connection.reqAllOpenOrders()
        connection.reqAutoOpenOrders()
        connection.reqNewsBulletins()
        ## connection.reqManagedAccts()

        #exec_filter = ib.types.ExecutionFilter(secType='FUT')
        #connection.reqExecutions(exec_filter)
    
        for tickerSym, tickerId in self.tickers.items():
            contract = ib.types.Contract(symbol=tickerSym,
                                         secType='STK',
                                         exchange="SMART",
                                         currency='USD')
            connection.reqMktData(tickerId, contract)
            connection.reqMktDepth(tickerId, contract)


    def demo100_SubmitOrders(self):
        """ submit an order for some stock

        """
        ## have to snooze in order to get the next order id
        time.sleep(self.snooze)

        self.handler.orderId += 1
        contract = ib.types.Contract(symbol=self.tickers.keys()[0],
                                     secType='STK',
                                     exchange="SMART",
                                     currency='USD',
                                     )
        order = ib.types.Order(orderId=self.handler.orderId, totalQuantity=100,
                               action='BUY',
                               primaryExch='ISLAND',
                               lmtPrice=12.00,
                               orderType='LMT')
        self.orderInfo = (self.handler.orderId, contract, order)
        self.connection.placeOrder(self.handler.orderId, contract, order)


    def demo101_SubmitOrdersWithComboLegs(self):
        """ submit an order for a futures contract with multiple combo legs

        """
        es_id = self.es_id
        cleg = ib.types.ComboLeg
        legs = [
            cleg(es_id, ratio=1, action='BUY', exchange='GLOBEX', openClose=0),
            cleg(es_id, ratio=2, action='BUY', exchange='GLOBEX', openClose=1),
            cleg(es_id, ratio=3, action='SELL', exchange='GLOBEX', openClose=2),
        ]
        self.handler.orderId += 1
        order = ib.types.Order(orderId=self.handler.orderId, totalQuantity=1, lmtPrice=1200, orderType="LMT")
        self.connection.placeOrder(self.handler.orderId, self.es_contract, order)


    def demo102_CancelOrder(self):
        """ submit a silly order and then cancel it

        """
        time.sleep(self.snooze)
        try:
            self.connection.cancelOrder(self.orderInfo[0])
        except (AttributeError, ):
            pass


    def demo200_RequestContractDetails(self):
        """ request market data and market details for a futures contract

        """
        self.es_id = es_id = next_tickerId()
        self.es_contract = contract = \
            ib.types.Contract(symbol='ES', secType='FUT', exchange='GLOBEX',
                             expiry='200603')

        self.connection.reqMktData(es_id, contract)
        self.connection.reqContractDetails(contract)


    def demo201_RequestHistoricalData(self):
        """ request historical market data

        """
        id = next_tickerId()
        contract = ib.types.Contract(symbol='MSFT', secType='STK', exchange='SMART')
        endDateTime = time.strftime('%Y%m%d %H:%M:%S GMT')
        return
        self.connection.reqHistoricalData(id,
                                          contract,
                                          endDateTime,
                                          '300 S',
                                          5,
                                          'BID',
                                          1,
                                          2)


    def demo202_CancelMarketData(self):
        """ 

        """
        connection = self.connection

        for tickerSym, tickerId in self.tickers.items():
            connection.cancelMktData(tickerId)
            connection.cancelMktDepth(tickerId)

        connection.cancelNewsBulletins()


def ids(next):
    """ ids(...) -> an id generator """
    while True:
        yield next
        next += 1


## one id generator for connections and another for tickers
next_connection_id = ids(0).next
next_tickerId = ids(5000).next


if __name__ == '__main__':
    try:
        __IP
    except (NameError, ):
        os.environ['PYTHONINSPECT'] = '1'
    raw_input('Start TWS and login before continuing.  Press enter when ready.')
    demo = AutomaticDemoApp()
n
