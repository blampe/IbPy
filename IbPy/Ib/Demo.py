#!/usr/bin/env python
""" Ib.Demo -> a module not unlike a demo, a module not unlike a unittest

The DemoHandler and DemoApp classes show a simplistic way of constructing an 
application that uses IbPy.  The DemoApp class constructs an IbPy.Socket 
connection, a DemoHandler, and makes the association between the two.

These two classes also form a unit test of sorts.  I'm not exactly certain of 
the best testing approach to take with IbPy and TWS, but this is allows me to
execute most of the IbPy code and interact with it at the Python prompt. YMMV.

"""
import os
import sys
import time

import Ib.Message
import Ib.Socket
import Ib.Type


class DemoHandler(object):
    """ DemoHandler() -> defines methods suitable for IbPy callbacks

    """
    def __init__(self):
        self.events = {}
        self.order_id = 0

    def connected(self, event):
        """ connected(event) -> executed when IbPy connects to TWS

        """
        print 'connected', event

    def disconnected(self, event):
        """ disconnected(event) -> executed when IbPy disconnects from TWS

        """
        print 'disconnected', event

    def assert_event(self, event_type, event):
        """ assert_event(...) -> checks the events attributes

        """
        for slot in event_type.EventDetail.__slots__:
            assert hasattr(event, slot)

    ##
    ## the reuse via copy and paste below is lame, true, but the intent is to
    ## show how to implement separate handlers for the various types of IbPy
    ## events, not to reuse code.
    ## 

    def account_updated(self, event):
        """ account_updated(event) -> called when account values change

        """
        self.assert_event(Ib.Message.Account, event)
        self.events.setdefault(co_name(), []).append(event)
        print 'Account value changed: %s is %s' % (event.key, event.value, )

    def error(self, event):
        """ error(event) -> called when TWS reports an error

        """
        self.assert_event(Ib.Message.Error, event)
        self.events.setdefault(co_name(), []).append(event)
        err = (event.error_id, event.error_code, event.error_msg, )
        print 'An Error from TWS: %s %s %s' % err

    def ticker_updated(self, event):
        """ ticker_updated(event) -> called when ticker price or size data has changed

        """
        self.assert_event(Ib.Message.Ticker, event)
        self.events.setdefault(co_name(), []).append(event)

    def next_order_id(self, event):
        """ next_order_id(event) -> called to tell us the first usable order id

        """
        self.assert_event(Ib.Message.NextId, event)
        self.events.setdefault(co_name(), []).append(event)
        self.order_id = event.next_valid_id

    def order_status(self, event):
        """ order_status(event) -> called when the status of an order has changed

        """
        self.assert_event(Ib.Message.OrderStatus, event)
        self.events.setdefault(co_name(), []).append(event)
        ordinfo = (event.order_id, event.message, )
        print 'Order status changed:  order id %s, status %s' % ordinfo

    def open_order(self, event):
        """ open_order(event) -> called once for every existing order upon connection

        """
        self.assert_event(Ib.Message.OpenOrder, event)
        self.events.setdefault(co_name(), []).append(event)

    def contract_details(self, event):
        """ contract_details(event) -> called with details on a contract

        """
        self.assert_event(Ib.Message.ContractDetails, event)
        self.events.setdefault(co_name(), []).append(event)

    def managed_accounts(self, event):
        """ managed_accounts(event) -> called with a list of accounts manage

        """
        self.assert_event(Ib.Message.ManagedAccounts, event)
        self.events.setdefault(co_name(), []).append(event)

    def news_bulletin(self, event):
        """ news_bulletin(event) -> called when there is news!

        """
        self.assert_event(Ib.Message.NewsBulletin, event)
        self.events.setdefault(co_name(), []).append(event)

    def exec_details(self, event):
        """ exec_details(event) -> called with execution details

        """
        self.assert_event(Ib.Message.ExecutionDetails, event)
        self.events.setdefault(co_name(), []).append(event)

    def portfolio_updated(self, event):
        """ portfolio_updated(event) -> called when the portfolio has changed

        """
        self.assert_event(Ib.Message.Portfolio, event)
        self.events.setdefault(co_name(), []).append(event)

    def register_handler(self, conn):
        """ register_handler(conn) -> register the methods of this object

        """
        conn.register(Ib.Message.Account, self.account_updated)
        conn.register(Ib.Message.ContractDetails, self.contract_details)
        conn.register(Ib.Message.Error, self.error)
        conn.register(Ib.Message.ExecutionDetails, self.exec_details)
        conn.register(Ib.Message.ManagedAccounts, self.managed_accounts)
        conn.register(Ib.Message.NextId, self.next_order_id)
        conn.register(Ib.Message.NewsBulletin, self.news_bulletin)
        conn.register(Ib.Message.OpenOrder, self.open_order)
        conn.register(Ib.Message.OrderStatus, self.order_status)
        conn.register(Ib.Message.Portfolio, self.portfolio_updated)
        conn.register(Ib.Message.ReaderStart, self.connected)
        conn.register(Ib.Message.ReaderStop, self.disconnected)
        conn.register(Ib.Message.Ticker, self.ticker_updated)


class DemoApp(object):
    """ DemoApp() -> 

    """
    def __init__(self, dsn=('localhost', 7496), server_log_level=3, 
                 settle_seconds=3):
        self.server_log_level = server_log_level
        self.settle_seconds = settle_seconds
        self.tickers = [
            (next_ticker_id(), 'AAPL'),
            (next_ticker_id(), 'MXIM'),
        ]

        self.connection = connection = Ib.Socket.build(next_connection_id())
        self.handler = handler = DemoHandler()
        handler.register_handler(connection)
        connection.connect(dsn)

        ## get and execute all the demo methods
        names = [getattr(self, n) for n in dir(self) if n.startswith('demo_')]
        names.sort()
        for func in names:
            func()

    def demo_b_request(self):
        """ make requests for account data, ticker data, etc.

        """
        connection = self.connection
        connection.set_server_log_level(self.server_log_level)
        connection.request_account_updates()
        connection.request_open_orders()
        connection.request_all_open_orders()
        connection.request_auto_open_orders()
        connection.request_news_bulletins()
        connection.request_managed_accounts()

        exec_filter = Ib.Type.ExecutionFilter(sec_type='FUT')
        connection.request_executions(exec_filter)

        for ticker_id, symbol in self.tickers:
            contract = Ib.Type.Contract(symbol=symbol, sec_type='STK')
            connection.request_market_data(ticker_id, contract)
            connection.request_market_depth(ticker_id, contract)

    def demo_c_order(self):
        """ submit an order for some stock

        """
        ## have to snooze in order to get the next order id
        time.sleep(self.settle_seconds) 

        self.handler.order_id += 1
        contract = Ib.Type.Contract(symbol=self.tickers[0][1], sec_type='STK')
        order = Ib.Type.Order(order_id=self.handler.order_id, quantity=200, 
                              limit_price=24.00)
        self.connection.place_order(self.handler.order_id, contract, order)

    def demo_d_contract(self):
        """ request market data and market details for a futures contract

        """
        self.es_id = es_id = next_ticker_id()
        self.es_contract = contract = \
            Ib.Type.Contract(symbol='ES', sec_type='FUT', exchange='GLOBEX',
                             expiry='200403')

        self.connection.request_market_data(es_id, contract)
        self.connection.request_contract_details(contract)

    def demo_e_combo_legs(self):
        """ submit an order for a futures contract with multiple combo legs

        """
        es_id = self.es_id
        cleg = Ib.Type.ComboLeg
        legs = [
            cleg(es_id, ratio=1, action='BUY', exchange='GLOBEX', open_close=0),
            cleg(es_id, ratio=2, action='BUY', exchange='GLOBEX', open_close=1),
            cleg(es_id, ratio=3, action='SELL', exchange='GLOBEX', open_close=2),
        ]
        self.handler.order_id += 1
        order = Ib.Type.Order(order_id=self.handler.order_id, quantity=1, limit_price=1200)
        self.connection.place_order(self.handler.order_id, self.es_contract, order)

    def demo_f_cancelled_order(self):
        """ submit a silly order and then cancel it

        """
        self.handler.order_id += 1
        contract = Ib.Type.Contract(symbol=self.tickers[0][1], sec_type='STK')
        order = Ib.Type.Order(order_id=self.handler.order_id, quantity=1, limit_price=3.00)
        self.connection.place_order(self.handler.order_id, contract, order)
        time.sleep(self.settle_seconds)
        self.connection.cancel_order(self.handler.order_id)

    def cancel_some_requests(self):
        """ cancel_some_requests() -> stop the market data and market depth feeds

        """
        connection = self.connection

        for ticker_id, symbol in self.tickers:
            connection.cancel_market_data(ticker_id)
            connection.cancel_market_depth(ticker_id)

        connection.cancel_news_bulletins()

    def disconnect(self):
        """ if this was a testcase subclass this would be named tearDown

        """
        self.connection.disconnect()


def co_name(index=1):
    """ co_name(index=1) -> the name of the caller indicated by the frame index

    """
    return sys._getframe(index).f_code.co_name


def next_connection_id(connection_id=0):
    """ next_connection_id(...) -> a connection id generator

    """
    while True:
        yield connection_id
        connection_id += 1


def next_ticker_id(ticker_id=100):
    """ next_ticker_id(...) -> a ticker id generator

    """
    while True:
        yield ticker_id
        ticker_id += 1


## module-level singletons
next_connection_id = next_connection_id().next
next_ticker_id = next_ticker_id().next


if __name__ == '__main__':
    banner = 'start tws and login before continuing'
    try:
        ## support for the enhanced ipython shell...
        __IP
        print >> sys.__stdout__, banner
    except (NameError, ):
        ## ... vs. the regular python shell
        os.environ['PYTHONINSPECT'] = '1'
        raw_input(banner)

    demo = DemoApp()
