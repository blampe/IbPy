#!/usr/bin/env python
""" Ib.Socket -> Interactive Brokers socket connection and threaded reader


"""
import socket
import struct
import threading

import Ib.Message
import Ib.Type


SERVER_VERSION = 1
CLIENT_VERSION = 10

READER_START = -1
READER_STOP = -2

(BID_SIZE, BID_PRICE, ASK_PRICE, ASK_SIZE, LAST_PRICE, LAST_SIZE, HIGH_PRICE,
 LOW_PRICE, VOLUME_SIZE, CLOSE_PRICE) = range(0, 10)

(TICK_PRICE, TICK_SIZE, ORDER_STATUS, ERR_MSG, OPEN_ORDER,  ACCT_VALUE,
 PORTFOLIO_VALUE, ACCT_UPDATE_TIME, NEXT_VALID_ID, CONTRACT_DATA,
 EXECUTION_DATA, MARKET_DEPTH, MARKET_DEPTH_L2, NEWS_BULLETINS,
 MANAGED_ACCTS) = range(1, 16)

(REQ_MKT_DATA, CANCEL_MKT_DATA, PLACE_ORDER, CANCEL_ORDER,
 REQ_OPEN_ORDERS, REQ_ACCOUNT_DATA, REQ_EXECUTIONS, REQ_IDS,
 REQ_CONTRACT_DATA, REQ_MKT_DEPTH, CANCEL_MKT_DEPTH,
 REQ_NEWS_BULLETINS, CANCEL_NEWS_BULLETINS, SET_SERVER_LOGLEVEL,
 REQ_AUTO_OPEN_ORDERS, REQ_ALL_OPEN_ORDERS, REQ_MANAGED_ACCTS) = range(1, 18)


class SocketReaderBase(object):
    """ SocketReaderBase(reader, socket) -> TWS socket data reader base class

    This class provides the logic for reading a socket when called to 'run()'.
    Subclasses mix this type in to the appropriate threading library type 
    (e.g., python threading.Thread or Qt QThread)
    """
    def __init__(self, readers, socket):
        object.__init__(self)
        self.active = 0
        self.readers = readers
        self.socket = socket

    def run(self):
        """ run() -> read socket data encoded by TWS 

        """
        ri, rf, rs = self.read_integer, self.read_float, self.read_string
        readers = self.readers
        readers[READER_START].dispatch()
        self.active = 1

        while self.active:
            ## swallow all exceptions for the client if/when
            ## the connection closes.  this also swallows any
            ## exceptions thrown by a reader function.
            try:
                msg_id = ri()
                readers[msg_id].read(ri, rf, rs)
            except (Exception, ), ex:
                self.last_exc = ex
                self.active = 0
                readers[READER_STOP].dispatch(exception='%s' % (ex, ))

    def read_integer(self):
        """ read_integer() -> read an integer from the socket

        """
        ivalue = self.read_string()
        try:
            return int(ivalue)
        except (ValueError, ):
            return 0

    def read_float(self):
        """ read_float() -> read and unpack a float from the socket

        """
        fvalue = self.read_string()
        try:
            return float(fvalue)
        except (ValueError, ):
            return 0.0

    def read_string(self):
        """ read_string() -> read and unpack a string from the socket

        """
        buf_size = 1
        read_bites = ['', ]
        read_func = self.socket.recv
        unpack = struct.unpack

        while True:
            socket_read = read_func(buf_size)
            bite = unpack('!s', socket_read)[0]
            if not ord(bite):
                break
            read_bites.append(socket_read)
        return ''.join(read_bites)


class SocketReader(threading.Thread, SocketReaderBase):
    """ SocketReader(...) -> bridge to the Python thread reader implementation

    """
    def __init__(self, readers, socket):
        SocketReaderBase.__init__(self, readers, socket)
        threading.Thread.__init__(self)
        self.setDaemon(True)


    def run(self):
        SocketReaderBase.run(self)


class SocketConnection(object):
    """ SocketConnection(reader, socket) -> useful wrapper of a socket for IB

        This type defines methods for requesting ticker data, account data, etc.

        When called to connect, this type constructs a python socket, connects 
        it to TWS, and if successful, creates and starts a reader object.  The
        reader object is then responsible for slurping data from the connection 
        and doing something with it.

        Many of the socket methods have 'other_version' and/or 'other_magic'
        references; these aren't documented by IB but their implementations
        use them just the same.  It seems that these version numbers change
        on a method-by-method basis, so abstracting them becomes misleading.
    """
    reader_types = {
        ACCT_VALUE : Ib.Message.AccountValue,
        ACCT_UPDATE_TIME : Ib.Message.AccountTime,
        CONTRACT_DATA : Ib.Message.ContractDetails,
        ERR_MSG : Ib.Message.Error,
        EXECUTION_DATA : Ib.Message.ExecutionDetails,
        MANAGED_ACCTS : Ib.Message.ManagedAccounts,
        MARKET_DEPTH : Ib.Message.MarketDepth,
        MARKET_DEPTH_L2 : Ib.Message.MarketDepthLevel2,
        NEWS_BULLETINS : Ib.Message.NewsBulletin,
        NEXT_VALID_ID : Ib.Message.NextId,
        OPEN_ORDER : Ib.Message.OpenOrder,
        ORDER_STATUS : Ib.Message.OrderStatus,
        PORTFOLIO_VALUE : Ib.Message.Portfolio,
        READER_START : Ib.Message.ReaderStart,
        READER_STOP : Ib.Message.ReaderStop,
        TICK_PRICE : Ib.Message.TickerPrice,
        TICK_SIZE : Ib.Message.TickerSize,
    }

    def __init__(self, client_id, reader_type):
        self.client_id = client_id
        self.server_version = 0
        self.reader_type = reader_type
        readers = self.reader_types.items()
        self.readers = dict([(msgid, reader()) for msgid, reader in readers])

    def connect(self, address, client_version=CLIENT_VERSION):
        """ connect((host, port)) -> construct a socket and connect it to TWS

        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reader = self.reader_type(self.readers, self.socket)
        self.socket.connect(address)

        self.send(client_version)
        self.server_version = self.reader.read_integer()
        self.send(self.client_id)
        self.reader.start()

    def disconnect(self):
        """ disconnect() -> close the socket.

            This causes an exception if the socket is active, but that exception
            gets caught by the stop reader.
        """
        self.socket.close()

    def request_market_data(self, ticker_id, contract):
        """ request_market_data(ticker_id, contract) -> request market data

            ticker_id will be used by the broker to refer to the market 
            instrument in subsequent communication.
        """
        other_version = 3
        data = (REQ_MKT_DATA, 
                other_version, 
                ticker_id, 
                contract.symbol,
                contract.sec_type, 
                contract.expiry, 
                contract.strike,
                contract.right, 
                contract.exchange, 
                contract.currency,
                contract.local_symbol, )
        map(self.send, data)
        self.send_combolegs(contract)

    def request_contract_details(self, contract):
        """ request_contract_details(contract) -> request contract details

        """
        other_version = 1
        data = (REQ_CONTRACT_DATA, 
                other_version, 
                contract.symbol,
                contract.sec_type, 
                contract.expiry, 
                contract.strike,
                contract.right, 
                contract.exchange, 
                contract.currency, 
                contract.local_symbol, )
        map(self.send, data)

    def request_market_depth(self, ticker_id, contract):
        """ request_market_depth(ticker_id, contract) -> request market depth

        """
        other_version = 1
        data = (REQ_MKT_DEPTH,
                other_version,
                ticker_id,
                contract.symbol,
                contract.sec_type,
                contract.expiry,
                contract.strike,
                contract.right,
                contract.exchange,
                contract.currency,
                contract.local_symbol)
        map(self.send, data)

    def cancel_market_data(self, ticker_id):
        """ cancel_market_data(ticker_id) -> cancel market data

        """
        other_version = 1
        data = (CANCEL_MKT_DATA,
                other_version,
                ticker_id)
        map(self.send, data)

    def cancel_market_depth(self, ticker_id):
        """ cancel_market_depth(ticker_id) -> cancel market depth

        """
        other_version = 1
        data = (CANCEL_MKT_DEPTH,
                other_version,
                ticker_id)
        map(self.send, data)

    def place_order(self, order_id, contract, order):
        """ place_order(order_id, contract, order) -> place an order

        """
        other_version = 7
        send = self.send
        map(send, (PLACE_ORDER,
                   other_version,
                   order_id))

        ## contract fields
        map(send, (contract.symbol,
                   contract.sec_type,
                   contract.expiry,
                   contract.strike,
                   contract.right,
                   contract.exchange,
                   contract.currency,
                   contract.local_symbol))

        ## main order fields
        map(send, (order.action,
                   order.quantity,
                   order.order_type,
                   order.limit_price,
                   order.aux_price))

        ## extended order fields
        map(send, (order.tif,
                   order.oca_group,
                   order.account,
                   order.open_close,
                   order.origin,
                   order.order_ref,
                   order.transmit,
                   order.parent_id))

        ## more extended order fields
        map(send, (order.block_order,
                   order.sweep_to_fill,
                   order.display_size,
                   order.trigger_method,
                   order.ignore_rth))

        send(order.hidden)
        self.send_combolegs(contract)
        send(order.shares_allocation)

    def request_account_updates(self, subscribe=1, acct_code=''):
        """ request_account_updates() -> request account data updates

        """
        other_version = 2
        map(self.send, (REQ_ACCOUNT_DATA,
                        other_version,
                        subscribe,
                        acct_code))

    def request_executions(self, exec_filter=None):
        """ request_executions() -> request order execution data

        """
        other_version = 2
        map(self.send, (REQ_EXECUTIONS, 
                        other_version))

        if exec_filter is None:
            exec_filter = Ib.Type.ExecutionFilter()

        map(self.send, (exec_filter.client_id,
                        exec_filter.acct_code,
                        exec_filter.time,
                        exec_filter.symbol,
                        exec_filter.sec_type,
                        exec_filter.exchange,
                        exec_filter.side))

    def cancel_order(self, order_id):
        """ cancel_order(order_id) -> cancel order specified by order_id

        """
        other_version = 1
        map(self.send, (CANCEL_ORDER,
                        other_version,
                        order_id))

    def request_open_orders(self):
        """ request_open_orders() -> request order data

        """
        other_version = 1
        map(self.send, (REQ_OPEN_ORDERS, other_version))

    def request_news_bulletins(self, all=True):
        """ request_news_bulletins(all=True) -> request news bulletin updates

        """
        other_version = 1
        map(self.send, (REQ_NEWS_BULLETINS, other_version, int(all)))

    def cancel_news_bulletins(self):
        """ cancel_news_bulletins() -> cancel news bulletin updates

        """
        other_version = 1
        map(self.send, (CANCEL_NEWS_BULLETINS, other_version))

    def set_server_log_level(self, level):
        """ set_server_log_level(level=[1..4]) -> set the server log verbosity

        """
        other_version = 1
        map(self.send, (SET_SERVER_LOGLEVEL, other_version, level))

    def request_auto_open_orders(self, auto_bind=True):
        """ request_auto_open_orders() -> request auto open orders

        """
        other_version = 1
        map(self.send, (REQ_AUTO_OPEN_ORDERS, other_version, int(auto_bind)))

    def request_all_open_orders(self):
        """ request_all_open_orders() -> request all open orders

        """
        other_version = 1
        map(self.send, (REQ_ALL_OPEN_ORDERS, other_version))

    def request_managed_accounts(self):
        """ request_managed_accounts() -> request managed accounts

        """
        other_version = 1
        map(self.send, (REQ_MANAGED_ACCTS, other_version))

    def send(self, data, packfunc=struct.pack, eof=struct.pack('!i', 0)[3]):
        """ send(data) -> send a value to TWS

        """
        sendfunc = self.socket.send
        for k in str(data):
            sendfunc(packfunc('!i', ord(k))[3])
        sendfunc(eof)

    def send_combolegs(self, contract):
        """ send_combolegs(contract) -> helper to send a contracts combo legs

        """
        if contract.combo_legs:
            send = self.send
            send(len(contract.combo_legs))
            for leg in contract.combo_legs:
                legvalues = (leg.con_id, leg.ratio, leg.action, leg.exchange, 
                             # is open_close a bug?  
                             # it's not sent in the ib sources
                             leg.open_close)
                map(send, legvalues)
        else:
            # why not self.send(0) like the ib implementation?
            pass 

    def register(self, message_type, listener):
        """ register(listener) -> add callable listener to message receivers

        """
        for msg_reader in self.readers.values():
            if isinstance(msg_reader , (message_type, )):
                if not msg_reader.listeners.count(listener):
                    msg_reader.listeners.append(listener)

    def deregister(self, message_type, listener):
        """ deregister(listener) -> remove listener from message receivers

        """
        for msg_reader in self.readers.values():
            if isinstance(msg_reader, (message_type, )):
                try:
                    msg_reader.listeners.remove(listener)
                except (ValueError, ):
                    pass


def build(client_id=0, reader_type=None):
    """ build(client_id) -> creates a new ib socket connection

    """
    reader_type = reader_type or SocketReader
    return SocketConnection(client_id=client_id, reader_type=reader_type)
