#!/usr/bin/env python
""" Ib.Demo -> a module not unlike a demo, a module not unlike a unittest

The SimpleMessageHandler and AutomaticDemoApp classes show a simplistic way of
constructing an application that uses IbPy.  The AutomaticDemoApp class
constructs an IbPy.Socket connection, a SimpleMessageHandler, and makes the
association between the two.

These two classes also form a unit test of sorts.  I'm not exactly certain of 
the best testing approach to take with IbPy and TWS, but this is allows me to
execute most of the IbPy code and interact with it at the Python prompt. YMMV.

"""
import os
import sys
import time

import ib.message
import ib.socket
import ib.type


class SimpleMessageHandler:
    """ SimpleMessageHandler() -> defines methods suitable for IbPy callbacks

    """
    order_id = 0    
    outstream = file('ibpy_demo_output.txt', 'w')
    
    def connected(self, msg):
        """ connected(msg) -> executed when IbPy connects to TWS

        """
        print >> self.outstream, 'connected', msg


    def disconnected(self, msg):
        """ disconnected(msg) -> executed when IbPy disconnects from TWS

        """
        print >> self.outstream, 'disconnected', msg


    def account_updated(self, msg):
        """ account_updated(msg) -> called when account values change

        """
        print >> self.outstream, 'Account value changed: %s is %s' % (msg.key, msg.value, )


    def error(self, msg):
        """ error(msg) -> called when TWS reports an error

        """
        err = (msg.error_id, msg.error_code, msg.error_msg, )
        print >> self.outstream, 'An Error from TWS: %s %s %s' % err


    def ticker_updated(self, msg):
        """ ticker_updated(msg) -> called when ticker price or size data has changed

        """
        print >> self.outstream, msg


    def next_order_id(self, msg):
        """ next_order_id(msg) -> called to tell us the first usable order id

        """
        self.order_id = msg.next_valid_id
        print >> self.outstream, msg


    def order_status(self, msg):
        """ order_status(msg) -> called when order status has changed

        """
        ordinfo = (msg.order_id, msg.message, )
        print >> self.outstream, 'Order status changed:  order id %s, status %s' % ordinfo


    def open_order(self, msg):
        """ open_order(msg) -> called for every existing order

        """


    def contract_details(self, msg):
        """ contract_details(msg) -> called with details on a contract

        """
        print >> self.outstream, msg


    def managed_accounts(self, msg):
        """ managed_accounts(msg) -> called with a list of accounts manage

        """


    def news_bulletin(self, msg):
        """ news_bulletin(msg) -> called when there is news!

        """


    def exec_details(self, msg):
        """ exec_details(msg) -> called with execution details

        """


    def portfolio_updated(self, msg):
        """ portfolio_updated(msg) -> called when the portfolio has changed

        """


    def historical_data(self, msg):
        print >> self.outstream, msg


class AutomaticDemoApp:
    """ AutomaticDemoApp() -> something not unlike a demonstration.

    """
    def __init__(self, dsn=('localhost', 7496), log_level=3, snooze=3):
        self.log_level = log_level
        self.snooze = snooze
        self.tickers = [
            (next_ticker_id(), 'AAPL'),
            (next_ticker_id(), 'MXIM'),
        ]

        self.connection = ib.socket.build(next_connection_id())
        self.build_handler()
        self.connection.connect(dsn)

        ## get and execute all the demo methods
        funcs = [getattr(self, n) for n in dir(self) if n.startswith('demo_')]
        funcs.sort()
        for func in funcs:
            func()


    def build_handler(self):
        """ build_handler(conn) -> create a handler and register its methods

        """
        handler = self.handler = SimpleMessageHandler()
        register = self.connection.register

        register(ib.message.Account, handler.account_updated)
        register(ib.message.ContractDetails, handler.contract_details)
        register(ib.message.Error, handler.error)
        register(ib.message.ExecutionDetails, handler.exec_details)
        register(ib.message.ManagedAccounts, handler.managed_accounts)
        register(ib.message.NextId, handler.next_order_id)
        register(ib.message.NewsBulletin, handler.news_bulletin)
        register(ib.message.OpenOrder, handler.open_order)
        register(ib.message.OrderStatus, handler.order_status)
        register(ib.message.Portfolio, handler.portfolio_updated)
        register(ib.message.ReaderStart, handler.connected)
        register(ib.message.ReaderStop, handler.disconnected)
        register(ib.message.Ticker, handler.ticker_updated)
        register(ib.message.HistoricalData, handler.historical_data)
        
    def demo_b_request(self):
        """ make requests for account data, ticker data, etc.

        """
        connection = self.connection
        connection.set_server_log_level(self.log_level)
        connection.request_account_updates()
        connection.request_open_orders()
        connection.request_all_open_orders()
        connection.request_auto_open_orders()
        connection.request_news_bulletins()
        ## connection.request_managed_accounts()

        exec_filter = ib.type.ExecutionFilter(sec_type='FUT')
        connection.request_executions(exec_filter)

        for ticker_id, symbol in self.tickers:
            contract = ib.type.Contract(symbol=symbol, sec_type='STK')
            connection.request_market_data(ticker_id, contract)
            connection.request_market_depth(ticker_id, contract)


    def demo_c_order(self):
        """ submit an order for some stock

        """
        ## have to snooze in order to get the next order id
        time.sleep(self.snooze) 

        self.handler.order_id += 1
        contract = ib.type.Contract(symbol=self.tickers[0][1], sec_type='STK')
        order = ib.type.Order(order_id=self.handler.order_id, quantity=200, 
                              limit_price=24.00)
        self.connection.place_order(self.handler.order_id, contract, order)


    def demo_d_contract(self):
        """ request market data and market details for a futures contract

        """
        self.es_id = es_id = next_ticker_id()
        self.es_contract = contract = \
            ib.type.Contract(symbol='ES', sec_type='FUT', exchange='GLOBEX',
                             expiry='200603')

        self.connection.request_market_data(es_id, contract)
        self.connection.request_contract_details(contract)


    def demo_d_historicaldata(self):
        """ request historical market data

        """
        id = next_ticker_id()
        contract = ib.type.Contract(symbol='MSFT', sec_type='STK', exchange='SMART')
        endDateTime = time.strftime('%Y%m%d %H:%M:%S')
        self.connection.reqHistoricalData(id, contract, endDateTime, '300 S', 5, 'BID', 1, 1)


    def demo_e_combo_legs(self):
        """ submit an order for a futures contract with multiple combo legs

        """
        es_id = self.es_id
        cleg = ib.type.ComboLeg
        legs = [
            cleg(es_id, ratio=1, action='BUY', exchange='GLOBEX', open_close=0),
            cleg(es_id, ratio=2, action='BUY', exchange='GLOBEX', open_close=1),
            cleg(es_id, ratio=3, action='SELL', exchange='GLOBEX', open_close=2),
        ]
        self.handler.order_id += 1
        order = ib.type.Order(order_id=self.handler.order_id, quantity=1, limit_price=1200)
        self.connection.place_order(self.handler.order_id, self.es_contract, order)


    def demo_f_cancelled_order(self):
        """ submit a silly order and then cancel it

        """
        self.handler.order_id += 1
        contract = ib.type.Contract(symbol=self.tickers[0][1], sec_type='STK')
        order = ib.type.Order(order_id=self.handler.order_id, quantity=1, limit_price=3.00)
        self.connection.place_order(self.handler.order_id, contract, order)
        time.sleep(self.snooze)
        self.connection.cancel_order(self.handler.order_id)


    def demo_g_cancel_some_requests(self):
        """ cancel_some_requests() -> stop the market data and market depth feeds

        """
        connection = self.connection

        for ticker_id, symbol in self.tickers:
            connection.cancel_market_data(ticker_id)
            connection.cancel_market_depth(ticker_id)

        connection.cancel_news_bulletins()


    def disconnect(self):
        """ disconnect() -> tell the socket to disconnect

        """
        self.connection.disconnect()


def ids(next):
    """ ids(...) -> an id generator """
    while True:
        yield next
        next += 1


## one id generator for connections and another for tickers
next_connection_id = ids(0).next
next_ticker_id = ids(3000).next


if __name__ == '__main__':
    try:
        __IP
    except (NameError, ):
        os.environ['PYTHONINSPECT'] = '1'

    if int(os.environ.get('IBPY_LOGLEVEL', 20)) in range(1, 21):
        raw_input('Logger will print all messages.  Press enter.')
    else:
        SimpleMessageHandler.outstream = sys.stdout

    raw_input('Start TWS and login before continuing.  Press enter when ready.')

    ## see?  it runs by itself.
    demo = AutomaticDemoApp()
