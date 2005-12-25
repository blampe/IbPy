#!/usr/bin/env python
""" Ib.Socket -> Interactive Brokers socket connection and threaded reader


"""
import socket
import struct
import threading

import Ib.Logger
import Ib.Message
import Ib.Type


SERVER_VERSION = 1
CLIENT_VERSION = 17

READER_START = -1
READER_STOP = -2

(TICK_PRICE, TICK_SIZE, ORDER_STATUS, ERR_MSG, OPEN_ORDER,  ACCT_VALUE,
 PORTFOLIO_VALUE, ACCT_UPDATE_TIME, NEXT_VALID_ID, CONTRACT_DATA,
 EXECUTION_DATA, MARKET_DEPTH, MARKET_DEPTH_L2, NEWS_BULLETINS,
 MANAGED_ACCTS, RECEIVE_FA) = range(1, 17)

(REQ_MKT_DATA, CANCEL_MKT_DATA, PLACE_ORDER, CANCEL_ORDER,
 REQ_OPEN_ORDERS, REQ_ACCOUNT_DATA, REQ_EXECUTIONS, REQ_IDS,
 REQ_CONTRACT_DATA, REQ_MKT_DEPTH, CANCEL_MKT_DEPTH,
 REQ_NEWS_BULLETINS, CANCEL_NEWS_BULLETINS, SET_SERVER_LOGLEVEL,
 REQ_AUTO_OPEN_ORDERS, REQ_ALL_OPEN_ORDERS, REQ_MANAGED_ACCTS,
 REQ_FA, REPLACE_FA) = range(1, 20)

logger = Ib.Logger.logger()


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
        logger.debug('Created %s with fd %s', self, socket.fileno())
        
    def run(self):
        """ run() -> read socket data encoded by TWS 

        """
        logger.debug('Begin run %s', self)
        ri, rf, rs = self.read_integer, self.read_float, self.read_string
        readers = self.readers
        readers[READER_START].dispatch()
        self.active = 1

        while self.active:
            try:
                msg_id = ri()
                if msg_id == -1:
                    continue

                reader = readers[msg_id]
                logger.info('Message name=%s', reader)
                reader.read(ri, rf, rs)
            except (Exception, ), ex:
                self.active = 0
                logger.error('Exception %s during message dispatch', ex)
                readers[READER_STOP].dispatch(exception='%s' % (ex, ))
                logger.debug('Reader stop message dispatched')

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
        read_bites = []
        read_func = self.socket.recv
        unpack = struct.unpack

        while True:
            socket_read = read_func(buf_size)
            bite = unpack('!s', socket_read)[0]
            if not ord(bite):
                break
            read_bites.append(socket_read)

        read = ''.join(read_bites)
        logger.debug('Socket read bytes %s', read_bites)
        return read


class SocketReader(threading.Thread, SocketReaderBase):
    """ SocketReader(...) -> bridge to the Python thread reader implementation

    """
    def __init__(self, readers, socket):
        threading.Thread.__init__(self)
        SocketReaderBase.__init__(self, readers, socket)
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
    """
    reader_types = {
        ACCT_VALUE : Ib.Message.AccountValue,
        ACCT_UPDATE_TIME : Ib.Message.AccountTime,
        CONTRACT_DATA : Ib.Message.ContractDetails,
        ERR_MSG : Ib.Message.Error,
        EXECUTION_DATA : Ib.Message.ExecutionDetails,
        RECEIVE_FA : Ib.Message.ReceiveFa,
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

        # this enables the ticker price message handler to call our tick
        # size handlder
        self.readers[TICK_PRICE].sizer = self.readers[TICK_SIZE]

    def connect(self, address, client_version=CLIENT_VERSION):
        """ connect((host, port)) -> construct a socket and connect it to TWS

        """
        logger.debug('Creating socket object for %s', self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logger.debug('Creating reader of type %s for %s', self.reader_type, self)
        self.reader = self.reader_type(self.readers, self.socket)

        logger.info('Connecting object %s to address %s', self, address)
        self.socket.connect(address)

        logger.info('Sending client version %s', client_version)
        self.send(client_version)

        logger.info('Reading server version')
        self.server_version = self.reader.read_integer()
        logger.debug('Read server version %s', self.server_version)

        if self.server_version >= 3:
            logger.info('Sending client id %s for object %s', self.client_id, self)
            self.send(self.client_id)

        logger.debug('Starting reader for object %s', self)
        self.reader.start()

    def disconnect(self):
        """ disconnect() -> close the socket.

            This causes an exception if the socket is active, but that exception
            gets caught by the stop reader.
        """
        logger.debug('Closing socket on object %s', self)
        self.socket.close()
        logger.debug('Socked closed on object %s', self)

    def request_market_data(self, ticker_id, contract):
        """ request_market_data(ticker_id, contract) -> request market data

            ticker_id will be used by the broker to refer to the market 
            instrument in subsequent communication.
        """
        logger.debug('Requesting market data for ticker %s %s', ticker_id, contract.symbol)
        send = self.send
        server_version = self.server_version
        
        message_version = 5
        data = (REQ_MKT_DATA, 
                message_version, 
                ticker_id, 
                contract.symbol,
                contract.sec_type, 
                contract.expiry, 
                contract.strike,
                contract.right)
        map(send, data)

        if server_version >= 15:
            send(contract.multiplier)

        send(contract.exchange)

        if server_version >= 14:
            send(contract.primary_exchange)

        send(contract.currency)

        if server_version >= 2:
            send(contract.local_symbol)

        self.send_combolegs(contract)            
        logger.debug('Market data request for ticker %s %s sent', ticker_id, contract.symbol)

    def request_contract_details(self, contract):
        """ request_contract_details(contract) -> request contract details

        """
        server_version = self.server_version
        need_version = 4
        if server_version < need_version:
            ## TODO:  log or raise
            logger.warning('Did not send request for contract details server version mismatch %s %s', need_version, server_version)
            return

        send = self.send
        message_version = 2
        data = (REQ_CONTRACT_DATA, 
                message_version, 
                contract.symbol,
                contract.sec_type, 
                contract.expiry, 
                contract.strike,
                contract.right)
        map(send, data)

        if server_version >= 15:
            send(contract.multiplier)

        data = (contract.exchange, 
                contract.currency, 
                contract.local_symbol, )
        map(send, data)        

    def request_market_depth(self, ticker_id, contract):
        """ request_market_depth(ticker_id, contract) -> request market depth

        """
        server_version = self.server_version
        send = self.send
        
        if server_version < 6:
            ## TODO:  log or raise
            return
        
        message_version = 2
        data = (REQ_MKT_DEPTH,
                message_version,
                ticker_id,
                contract.symbol,
                contract.sec_type,
                contract.expiry,
                contract.strike,
                contract.right)
        map(send, data)

        if server_version >= 15:
            send(contract.multiplier)

        data = (contract.exchange,
                contract.currency,
                contract.local_symbol)
        map(send, data)

    def cancel_market_data(self, ticker_id):
        """ cancel_market_data(ticker_id) -> cancel market data

        """
        message_version = 1
        data = (CANCEL_MKT_DATA,
                message_version,
                ticker_id)
        map(self.send, data)

    def cancel_market_depth(self, ticker_id):
        """ cancel_market_depth(ticker_id) -> cancel market depth

        """
        if self.server_version < 6:
            ## TODO:  log or raise
            return
        
        message_version = 1
        data = (CANCEL_MKT_DEPTH,
                message_version,
                ticker_id)
        map(self.send, data)

    def place_order(self, order_id, contract, order):
        """ place_order(order_id, contract, order) -> place an order

        """
        server_version = self.server_version
        send = self.send
        message_version = 15

        map(send, (PLACE_ORDER,
                   message_version,
                   order_id))

        ## contract fields
        map(send, (contract.symbol,
                   contract.sec_type,
                   contract.expiry,
                   contract.strike,
                   contract.right))

        if server_version >= 15:
            send(contract.multiplier)

        send(contract.exchange)

        if server_version >= 14:
            send(contract.primary_exchange)

        send(contract.currency)

        if server_version >= 2:
            send(contract.local_symbol)

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
                   order.transmit))

        if server_version >= 4:
            send(order.parent_id)

        ## more extended order fields
        if server_version >= 5:
            map(send, (order.block_order,
                       order.sweep_to_fill,
                       order.display_size,
                       order.trigger_method,
                       order.ignore_rth))

        if server_version >= 7:
            send(order.hidden)

        if server_version >= 8 and contract.sec_type.lower() == 'bag':
            ## version check is done here:
            self.send_combolegs(contract)

        if server_version >= 9:
            send(order.shares_allocation)
            
        if server_version >= 10:
            send(order.discretionary_amount)

        if server_version >= 11:
            send(order.good_after_time)

        if server_version >= 12:
            send(order.good_till_date)

        if server_version >= 13:
            map(send, (order.fa_group,
                       order.fa_method,
                       order.fa_percentage,
                       order.fa_profile))

    def request_account_updates(self, subscribe=1, acct_code=''):
        """ request_account_updates() -> request account data updates

        """
        send = self.send
        message_version = 2

        map(send, (REQ_ACCOUNT_DATA,
                   message_version,
                   subscribe))

        if self.server_version >= 9:
            send(acct_code)

    def request_executions(self, exec_filter=None):
        """ request_executions() -> request order execution data

        """
        send = self.send
        message_version = 2

        map(send, (REQ_EXECUTIONS, 
                   message_version))

        if self.server_version >= 9:
            if exec_filter is None:
                exec_filter = Ib.Type.ExecutionFilter()

            map(send, (exec_filter.client_id,
                       exec_filter.acct_code,
                       exec_filter.time,
                       exec_filter.symbol,
                       exec_filter.sec_type,
                       exec_filter.exchange,
                        exec_filter.side))

    def cancel_order(self, order_id):
        """ cancel_order(order_id) -> cancel order specified by order_id

        """
        message_version = 1
        map(self.send, (CANCEL_ORDER,
                        message_version,
                        order_id))

    def request_open_orders(self):
        """ request_open_orders() -> request order data

        """
        message_version = 1
        map(self.send, (REQ_OPEN_ORDERS, message_version))

    def request_ids(self, count):
        """ request_ids() -> request ids

        """
        message_version = 1
        map(self.send, (REQ_IDS, message_version, count))
        
    def request_news_bulletins(self, all=True):
        """ request_news_bulletins(all=True) -> request news bulletin updates

        """
        message_version = 1
        map(self.send, (REQ_NEWS_BULLETINS, message_version, int(all)))

    def cancel_news_bulletins(self):
        """ cancel_news_bulletins() -> cancel news bulletin updates

        """
        message_version = 1
        map(self.send, (CANCEL_NEWS_BULLETINS, message_version))

    def set_server_log_level(self, level):
        """ set_server_log_level(level=[1..4]) -> set the server log verbosity

        """
        message_version = 1
        map(self.send, (SET_SERVER_LOGLEVEL, message_version, level))

    def request_auto_open_orders(self, auto_bind=True):
        """ request_auto_open_orders() -> request auto open orders

        """
        message_version = 1
        map(self.send, (REQ_AUTO_OPEN_ORDERS, message_version, int(auto_bind)))

    def request_all_open_orders(self):
        """ request_all_open_orders() -> request all open orders

        """
        message_version = 1
        map(self.send, (REQ_ALL_OPEN_ORDERS, message_version))

    def request_managed_accounts(self):
        """ request_managed_accounts() -> request managed accounts

        """
        message_version = 1
        map(self.send, (REQ_MANAGED_ACCTS, message_version))

    def request_fa(self, fa_type):
        """ request_fa(fa_type) -> request fa of some type

        """
        if self.server_version < 13:
            ## TODO:  log or raise
            return

        message_version = 1
        map(self.send, (REQ_FA, message_version, fa_type))

    def replace_fa(self, fa_type, xml):
        """ replace_fa(fa_type, xml) -> replace fa

        """
        if self.server_version < 13:
            ## TODO:  log or raise
            return

        message_version = 1
        map(self.send, (REPLACE_FA, message_version, fa_type, xml))

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
        send = self.send

        if self.server_version >= 8:
            if contract.combo_legs:
                send(len(contract.combo_legs))
                for leg in contract.combo_legs:
                    map(send, (leg.con_id,
                               leg.ratio,
                               leg.action,
                               leg.exchange,
                               leg.open_close))
            else:
                send(0)

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
