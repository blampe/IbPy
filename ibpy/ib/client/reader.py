#!/usr/bin/env python
""" ib.client.reader -> Interactive Brokers socket connection and reader


"""
import socket
import struct
import threading

import ib.lib
import ib.types
import ib.client.message


SERVER_VERSION = 1
CLIENT_VERSION = 27

BAG_SEC_TYPE = 'BAG'
GROUPS, PROFILES, ALIASES = range(1, 4)

READER_START = -1
READER_STOP = -2

(
TICK_PRICE, TICK_SIZE, ORDER_STATUS, ERR_MSG, OPEN_ORDER, ACCT_VALUE,
PORTFOLIO_VALUE, ACCT_UPDATE_TIME, NEXT_VALID_ID, CONTRACT_DATA,
EXECUTION_DATA, MARKET_DEPTH, MARKET_DEPTH_L2, NEWS_BULLETINS,
MANAGED_ACCTS, RECEIVE_FA, HISTORICAL_DATA, BOND_CONTRACT_DATA,
SCANNER_PARAMETERS, SCANNER_DATA
) = range(1, 21)
 
(
REQ_MKT_DATA, CANCEL_MKT_DATA, PLACE_ORDER, CANCEL_ORDER,
REQ_OPEN_ORDERS, REQ_ACCOUNT_DATA, REQ_EXECUTIONS, REQ_IDS,
REQ_CONTRACT_DATA, REQ_MKT_DEPTH, CANCEL_MKT_DEPTH,
REQ_NEWS_BULLETINS, CANCEL_NEWS_BULLETINS, SET_SERVER_LOGLEVEL,
REQ_AUTO_OPEN_ORDERS, REQ_ALL_OPEN_ORDERS, REQ_MANAGED_ACCTS, REQ_FA,
REPLACE_FA, REQ_HISTORICAL_DATA, EXERCISE_OPTIONS,
REQ_SCANNER_SUBSCRIPTION, CANCEL_SCANNER_SUBSCRIPTION,
REQ_SCANNER_PARAMETERS, CANCEL_HISTORICAL_DATA,
) = range(1, 26)

EOF = struct.pack('!i', 0)[3]

logger = ib.lib.logger()


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
        self.tokens = []
        self.lastdata = ''


    def run(self):
        """ run() -> read socket data encoded by TWS 

        """
        logger.debug('Begin %s', self)
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
                if str(reader) == 'Error':
                    log = logger.warning
                else:
                    log = logger.info
                log(reader)
                reader.read(ri, rf, rs)
            except (Exception, ), ex:
                self.active = 0
                logger.error('Exception %s during message dispatch', ex)
                readers[READER_STOP].dispatch(exception='%s' % (ex, ))
                logger.debug('Reader stop message dispatched')


    def read_integer(self):
        """ read_integer() -> read an integer from the socket

        """
        value = self.read_string()
        try:
            return int(value)
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


    def read_string__(self):
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


    def read_string(self):
        """ read_string() -> read and unpack a string from the socket

        """
        #do we need to get more tokens from the socket?
        buf_size = 2000
        while len(self.tokens)==0:
            data = self.socket.recv(buf_size)
            tokens = data.split('\x00')
            #.lastdata is the previous incomplete token
            tokens[0] = self.lastdata + tokens[0]
            self.lastdata = tokens.pop(-1)
            logger.debug('Socket read %d bytes, %d tokens',
                         len(data), len(tokens))
            self.tokens.extend(tokens)
            if len(self.tokens) > 0: break

        #ok, let's return the first token        
        return self.tokens.pop(0)


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
        ACCT_VALUE : ib.client.message.AccountValue,
        ACCT_UPDATE_TIME : ib.client.message.AccountTime,
        CONTRACT_DATA : ib.client.message.ContractDetails,
        ERR_MSG : ib.client.message.Error,
        EXECUTION_DATA : ib.client.message.Execution,
        RECEIVE_FA : ib.client.message.ReceiveFa,
        MANAGED_ACCTS : ib.client.message.ManagedAccounts,
        MARKET_DEPTH : ib.client.message.MarketDepth,
        MARKET_DEPTH_L2 : ib.client.message.MarketDepthLevel2,
        NEWS_BULLETINS : ib.client.message.NewsBulletin,
        NEXT_VALID_ID : ib.client.message.NextId,
        OPEN_ORDER : ib.client.message.OpenOrder,
        ORDER_STATUS : ib.client.message.OrderStatus,
        PORTFOLIO_VALUE : ib.client.message.Portfolio,
        READER_START : ib.client.message.ReaderStart,
        READER_STOP : ib.client.message.ReaderStop,
        TICK_PRICE : ib.client.message.TickerPrice,
        TICK_SIZE : ib.client.message.TickerSize,
        HISTORICAL_DATA : ib.client.message.HistoricalData,
        BOND_CONTRACT_DATA : ib.client.message.BondContractData,
        SCANNER_PARAMETERS : ib.client.message.ScannerParameters,
        SCANNER_DATA : ib.client.message.ScannerData,
    }


    def __init__(self, clientId, reader_type):
        self.clientId = clientId
        self.server_version = 0
        self.reader_type = reader_type

        readers = self.reader_types.items()
        self.readers = dict([(msgid, reader()) for msgid, reader in readers])

        # this enables the ticker price message handler to call our
        # tick size handlder
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

        if self.server_version>=20:
            tws_time = self.reader.read_string()
            logger.info('Received server TwsTime=%s', tws_time)

        if self.server_version >= 3:
            logger.info('Sending client id %s for object %s', self.clientId, self)
            self.send(self.clientId)

        logger.debug('Starting reader for object %s', self)
        self.reader.start()


    def disconnect(self):
        """ disconnect() -> close the socket.

        This causes an exception if the socket is active, but that
        exception gets caught by the stop reader.
        """
        logger.debug('Closing socket on object %s', self)
        self.socket.close()
        logger.debug('Socked closed on object %s', self)


    def request_market_data(self, ticker_id, contract):
        """ request_market_data(ticker_id, contract) -> request market data

        The ticker_id value will be used by the broker to refer to the
        market instrument in subsequent communication.
        """
        logger.debug('Requesting market data for ticker %s %s',
                     ticker_id, contract.symbol)
        send = self.send
        server_version = self.server_version
        
        message_version = 5
        data = (REQ_MKT_DATA, 
                message_version, 
                ticker_id, 
                contract.symbol,
                contract.secType, 
                contract.expiry, 
                contract.strike,
                contract.right)
        map(send, data)

        if server_version >= 15:
            send(contract.multiplier)
        send(contract.exchange)
        if server_version >= 14:
            send(contract.primaryExch)
        send(contract.currency)
        if server_version >= 2:
            send(contract.localSymbol)

        self.send_combolegs(contract)
        logger.debug('Market data request for ticker %s %s sent',
                     ticker_id, contract.symbol)


    def request_contract_details(self, contract):
        """ request_contract_details(contract) -> request contract details

        """
        server_version = self.server_version
        need_version = 4
        if server_version < need_version:
            msg = ('Did not send request for contract details '
                   'server version mismatch %s %s')
            logger.warning(msg, need_version, server_version)
            return

        send = self.send
        message_version = 2
        data = (REQ_CONTRACT_DATA, 
                message_version, 
                contract.symbol,
                contract.secType, 
                contract.expiry, 
                contract.strike,
                contract.right)
        map(send, data)

        if server_version >= 15:
            send(contract.multiplier)

        data = (contract.exchange, 
                contract.currency, 
                contract.localSymbol, )
        map(send, data)        


    def request_market_depth(self, ticker_id, contract, numRows=1):
        """ request_market_depth(ticker_id, contract) -> request market depth

        """
        server_version = self.server_version
        need_version = 6
        send = self.send
        if server_version < need_version:
            msg = ('Did not send request for market depth '
                   'server version mismatch %s %s')
            logger.warning(msg, need_version, server_version)
            return
        
        message_version = 3
        data = (REQ_MKT_DEPTH,
                message_version,
                ticker_id,
                contract.symbol,
                contract.secType,
                contract.expiry,
                contract.strike,
                contract.right)
        map(send, data)

        if server_version >= 15:
            send(contract.multiplier)

        data = (contract.exchange,
                contract.currency,
                contract.localSymbol)
        map(send, data)
        if server_version >= 19:
            send(numRows)


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


    def place_order(self, orderId, contract, order):
        """ place_order(orderId, contract, order) -> place an order

        """
        server_version = self.server_version
        send = self.send
        message_version = 20

        map(send, (PLACE_ORDER,
                   message_version,
                   orderId))

        ## contract fields
        map(send, (contract.symbol,
                   contract.secType,
                   contract.expiry,
                   contract.strike,
                   contract.right))
        if server_version >= 15:
            send(contract.multiplier)
        send(contract.exchange)
        if server_version >= 14:
            send(contract.primaryExch)
        send(contract.currency)
        if server_version >= 2:
            send(contract.localSymbol)

        ## main order fields
        map(send, (order.action,
                   order.totalQuantity,
                   order.orderType,
                   order.lmtPrice,
                   order.auxPrice))

        ## extended order fields
        map(send, (order.tif,
                   order.ocaGroup,
                   order.account,
                   order.openClose,
                   order.origin,
                   order.orderRef,
                   order.transmit))

        if server_version >= 4:
            send(order.parentId)

        ## more extended order fields
        if server_version >= 5:
            map(send, (order.blockOrder,
                       order.sweepToFill,
                       order.displaySize,
                       order.triggerMethod,
                       order.ignoreRth))

        if server_version >= 7:
            send(order.hidden)

        self.send_combolegs(contract)

        if server_version >= 9:
            send(order.sharesAllocation)
            
        if server_version >= 10:
            send(order.discretionaryAmt)

        if server_version >= 11:
            send(order.goodAfterTime)

        if server_version >= 12:
            send(order.goodTillDate)

        if server_version >= 13:
            map(send, (order.faGroup,
                       order.faMethod,
                       order.faPercentage,
                       order.faProfile))

        # institutional short sale slot fields.
        if server_version >= 18:  
            map(send, (order.shortSaleSlot,         # 0 only for retail, 1 or 2 only for institution.
                       order.designatedLocation))   # only populate when order.shortSaleSlot = 2

        if server_version >= 19:
            map(send, (
                       #order.faGroup,
                       order.ocaType,
                       order.rthOnly,
                       order.rule80A,
                       order.settlingFirm,
                       order.allOrNone))
            map(send, (order.minQty, order.percentOffset,))
            map(send, (order.eTradeOnly, order.firmQuoteOnly,))
            map(send, (order.nbboPriceCap, order.auctionStrategy, 
                          order.startingPrice, order.stockRefPrice,
                          order.delta))
            if server_version == 26:
                if order.orderType == 'VOL':
                    lower = order.stockRangeLower
                    upper = order.stockRangeUpper
                else:
                    upper = lower = ''
                map(send (upper, lower))
        
        if server_version >= 22:
            send(order.overridePercentageConstraints)

        if server_version >= 26:
            map(send, (order.volatility, order.volatilityType))
            if server_version < 28:
                send(order.deltaNeutralOrderType == 'MKT' and 1)
            else:
                send(order.deltaNeutralOrderType)
                send(order.deltaNeutralAuxPrice)
            send(order.continuousUpdate)
            if server_version == 26:
                map(send, (upper, lower))
            send(order.referencePriceType)


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
                exec_filter = ib.types.ExecutionFilter()

            map(send, (exec_filter.clientId,
                       exec_filter.acct_code,
                       exec_filter.time,
                       exec_filter.symbol,
                       exec_filter.secType,
                       exec_filter.exchange,
                       exec_filter.side))


    def cancel_order(self, orderId):
        """ cancel_order(orderId) -> cancel order specified by orderId

        """
        message_version = 1
        map(self.send, (CANCEL_ORDER,
                        message_version,
                        orderId))


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


    def reqHistoricalData(self, ticker_id, contract, endDateTime,
                         durationStr, barSizeSetting, whatToShow,
                         useRTH, formatDate):
        """

        """
        if self.server_version < 16:
            logger.warning('Server version mismatch.')
            return

        message_version = 3
        map(self.send, (REQ_HISTORICAL_DATA,
                        message_version,
                        ticker_id,
                        contract.symbol,
                        contract.secType,
                        contract.expiry,
                        contract.strike,
                        contract.right,
                        contract.multiplier,
                        contract.exchange,
                        contract.primaryExch,
                        contract.currency,
                        contract.localSymbol))
        if self.server_version >= 20:
            map(self.send, (endDateTime,
                            barSizeSetting))
        map(self.send, (durationStr,
                        useRTH,
                        whatToShow))
        if self.server_version > 16:
            self.send(formatDate)
        self.send_combolegs(contract)


    def cancelHistoricalData(self, ticker_id):
        """ cancelHistoricalData(ticker_id) ->

        """
        if self.server_version < 24:
            logger.warning('Server version mismatch.')
            return
        message_version = 1
        map(self.send, (CANCEL_HISTORICAL_DATA, message_version, ticker_id))


    def reqScannerParameters(self):
        """ reqScannerParameters() ->

        """
        if self.server_version < 24:
            logger.warning('Server version mismatch.')
            return
        message_version = 1
        map(self.send, (REQ_SCANNER_PARAMETERS, message_version))


    def reqScannerSubscription(self, ticker_id, subscription):
        """ reqScannerSubscription(subscription) ->

        """
        if self.server_version < 24:
            logger.warning('Server version mismatch.')            
            return
        message_version = 3
        map(self.send, (REQ_SCANNER_SUBSCRIPTION,
                        message_version,
                        ticker_id,
                        subscription.numberOfRows,
                        subscription.instrument,
                        subscription.locationCode,
                        subscription.scanCode,
                        subscription.abovePrice,
                        subscription.belowPrice,
                        subscription.aboveVolume,
                        subscription.marketCapAbove,
                        subscription.marketCapBelow,
                        subscription.moodyRatingAbove,
                        subscription.moodyRatingBelow,
                        subscription.spRatingAbove,
                        subscription.spRatingBelow,
                        subscription.maturityDateAbove,
                        subscription.maturityDateBelow,
                        subscription.couponRateAbove,
                        subscription.couponRateBelow,
                        subscription.excludeConvertible))
        if self.server_version >= 25:
            map(self.send, (subscription.averageOptionVolumeAbove,
                            subscription.scannerSetttingPairs))
        if self.server_version >= 27:
            map(self.send, (subscription.stockTypeFilter))


    def cancelScannerSubscription(self, ticker_id):
        """ cancelScannerSubscription(ticker_id) ->

        """
        if self.server_version < 24:
            ## TODO:  log or raise
            return
        message_version = 1
        map(self.send, (CANCEL_SCANNER_SUBSCRIPTION, message_version, ticker_id))


    def exerciseOptions(self, ticker_id, contract, exerciseAction,
                        exerciseQuantity, account, override):
        """ exerciseOptions(...) ->

        """
        if self.server_version < 21:
            logger.warning('Exercise Option API not supported')
            return
        message_version = 1
        map(self.send, (EXERCISE_OPTIONS,
                        message_version,
                        ticker_id,
                        contract.symbol,
                        contract.secType,
                        contract.expiry,
                        contract.strike,
                        contract.right,
                        contract.multiplier,
                        contract.exchange,
                        contract.currency,
                        contract.localSymbol,
                        exerciseAction,
                        exerciseQuantity,
                        account,
                        override))


    def send(self, data, packfunc=struct.pack):
        """ send(data) -> send a value to TWS

        """
        sendfunc = self.socket.send
        for k in str(data):
            sendfunc(packfunc('!i', ord(k))[3])
        sendfunc(EOF)


    def send_combolegs(self, contract):
        """ send_combolegs(contract) -> helper to send a contracts combo legs

        """
        send = self.send

        if self.server_version >= 8 and contract.secType.lower() == BAG_SEC_TYPE:
            if contract.comboLegs:
                send(len(contract.comboLegs))
                for leg in contract.comboLegs:
                    map(send, (leg.conId,
                               leg.ratio,
                               leg.action,
                               leg.exchange,
                               leg.openClose))
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


def build(clientId=0, reader_type=None):
    """ build(clientId) -> creates a new ib socket connection

    """
    reader_type = reader_type or SocketReader
    return SocketConnection(clientId=clientId, reader_type=reader_type)
