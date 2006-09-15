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
SCANNER_PARAMETERS, SCANNER_DATA, TICK_OPTION_COMPUTATION,
) = range(1, 22)
 
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


NO_API_FMT = 'Connected TWS version does not support %s API.'
NO_SCANNER_API = NO_API_FMT % 'scanner'
NO_CONTRACT_API = NO_API_FMT % 'contract details'
NO_DEPTH_API = NO_API_FMT % 'market depth'
NO_OPTION_EX_API = NO_API_FMT % 'options exercise'
NO_FA_API = NO_API_FMT % 'fa'


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
        ri, rf, rs = self.readInteger, self.readFloat, self.readString
        readers = self.readers
        readers[READER_START].dispatch()
        self.active = 1

        while self.active:
            try:
                msgId = ri()
                if msgId == -1:
                    continue
                reader = readers[msgId]

                if str(reader) == 'Error':
                    log = logger.warning
                else:
                    log = logger.info

                log(reader)
                reader.read(ri, rf, rs)

            except (Exception, ), ex:
                self.active = 0
                msg = 'Reading stopped on Exception %s during message dispatch'
                logger.error(msg, ex)
                readers[READER_STOP].dispatch(exception='%s' % (ex, ))


    def readInteger(self):
        """ readInteger() -> read an integer from the socket

        """
        value = self.readString()
        try:
            return int(value)
        except (ValueError, ):
            return 0


    def readFloat(self):
        """ readFloat() -> read and unpack a float from the socket

        """
        fvalue = self.readString()
        try:
            return float(fvalue)
        except (ValueError, ):
            return 0.0


    def readString__(self):
        """ readString() -> read and unpack a string from the socket

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


    def readString(self):
        """ readString() -> read and unpack a string from the socket

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
    readerTypes = {
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
        TICK_PRICE : ib.client.message.TickPrice,
        TICK_SIZE : ib.client.message.TickSize,
        HISTORICAL_DATA : ib.client.message.HistoricalData,
        BOND_CONTRACT_DATA : ib.client.message.BondContractData,
        SCANNER_PARAMETERS : ib.client.message.ScannerParameters,
        SCANNER_DATA : ib.client.message.ScannerData,
        TICK_OPTION_COMPUTATION : ib.client.message.TickOptionComputation,
    }


    def __init__(self, clientId, reader):
        self.clientId = clientId
        self.serverVersion = 0
        self.reader = reader

        readers = self.readerTypes.items()
        self.readers = dict([(msgid, reader()) for msgid, reader in readers])

        # this enables the ticker price message handler to call our
        # tick size handlder
        self.readers[TICK_PRICE].sizer = self.readers[TICK_SIZE]


    def connect(self, address, client_version=CLIENT_VERSION):
        """ connect((host, port)) -> construct a socket and connect it to TWS

        """
        debug = logger.debug
        debug('Creating socket object for %s', self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        debug('Creating reader of type %s for %s', self.reader, self)
        self.reader = self.reader(self.readers, self.socket)

        debug('Connecting object %s to address %s', self, address)
        self.socket.connect(address)

        debug('Sending client version %s', client_version)
        self.send(client_version)

        debug('Reading server version')
        self.serverVersion = self.reader.readInteger()
        logger.info('Read server version %s', self.serverVersion)

        if self.serverVersion>=20:
            tws_time = self.reader.readString()
            debug('Received server TwsTime=%s', tws_time)

        if self.serverVersion >= 3:
            debug('Sending client id %s for object %s', self.clientId, self)
            self.send(self.clientId)

        debug('Starting reader for object %s', self)
        self.reader.start()


    def disconnect(self):
        """ disconnect() -> close the socket.

        This causes an exception if the socket is active, but that
        exception gets caught by the stop reader.
        """
        logger.debug('Closing socket on object %s', self)
        self.socket.close()
        logger.debug('Socked closed on object %s', self)


    def cancelScannerSubscription(self, tickerId):
        """ cancelScannerSubscription(tickerId) -> cancel scanner subscription

        """
        if self.serverVersion < 24:
            logger.error(NO_SCANNER_API)
            return
        version = 1
        map(self.send, (CANCEL_SCANNER_SUBSCRIPTION, version, tickerId))


    def reqScannerParameters(self):
        """ reqScannerParameters() -> request scanner parameters

        """
        if self.serverVersion < 24:
            logger.error(NO_SCANNER_API)            
            return
        version = 1
        map(self.send, (REQ_SCANNER_PARAMETERS, version))


    def reqScannerSubscription(self, tickerId, subscription):
        """ reqScannerSubscription(subscription) -> request scanner subscription

        """
        if self.serverVersion < 24:
            logger.error(NO_SCANNER_API)
            return

        version = 3
        map(self.send, (REQ_SCANNER_SUBSCRIPTION,
                        version,
                        tickerId,
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
        if self.serverVersion >= 25:
            map(self.send, (subscription.averageOptionVolumeAbove,
                            subscription.scannerSetttingPairs))
        if self.serverVersion >= 27:
            map(self.send, (subscription.stockTypeFilter))


    def reqMktData(self, tickerId, contract):
        """ reqMktData(tickerId, contract) -> request market data

        The tickerId value will be used by the broker to refer to the
        market instrument in subsequent communication.
        """
        logger.debug('Requesting market data for ticker %s %s',
                     tickerId, contract.symbol)
        send = self.send
        serverVersion = self.serverVersion
        
        version = 5
        data = (REQ_MKT_DATA, 
                version, 
                tickerId, 
                contract.symbol,
                contract.secType, 
                contract.expiry, 
                contract.strike,
                contract.right)
        map(send, data)

        if serverVersion >= 15:
            send(contract.multiplier)
        send(contract.exchange)
        if serverVersion >= 14:
            send(contract.primaryExch)
        send(contract.currency)
        if serverVersion >= 2:
            send(contract.localSymbol)

        self.sendComboLegs(contract)
        msg = 'Market data request for ticker %s %s sent'
        logger.debug(msg, tickerId, contract.symbol)


    def cancelHistoricalData(self, tickerId):
        """ cancelHistoricalData(tickerId) ->

        """
        if self.serverVersion < 24:
            logger.error(NO_SCANNER_API)
            return
        version = 1
        map(self.send, (CANCEL_HISTORICAL_DATA, version, tickerId))


    def reqHistoricalData(self, tickerId, contract, endDateTime,
                         durationStr, barSizeSetting, whatToShow,
                         useRTH, formatDate):
        """ reqHistoricalData(...) -> request historical data

        """
        if self.serverVersion < 16:
            logger.warning('Server version mismatch.')
            return

        serverVersion = self.serverVersion
        send = self.send
        version = 3
        map(send, (REQ_HISTORICAL_DATA,
                   version,
                   tickerId,
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
        if serverVersion >= 20:
            map(send, (endDateTime, barSizeSetting))
        map(send, (durationStr, useRTH, whatToShow))
        if serverVersion > 16:
            send(formatDate)
        self.sendComboLegs(contract)


    def reqContractDetails(self, contract):
        """ reqContractDetails(contract) -> request contract details

        """
        serverVersion = self.serverVersion
        if serverVersion < 4:
            logger.warning(NO_CONTRACT_API)
            return

        send = self.send
        version = 2
        data = (REQ_CONTRACT_DATA, 
                version, 
                contract.symbol,
                contract.secType, 
                contract.expiry, 
                contract.strike,
                contract.right)
        map(send, data)

        if serverVersion >= 15:
            send(contract.multiplier)

        data = (contract.exchange, 
                contract.currency, 
                contract.localSymbol, )
        map(send, data)        


    def reqMktDepth(self, tickerId, contract, numRows=1):
        """ reqMktDepth(tickerId, contract) -> request market depth

        """
        serverVersion = self.serverVersion
        if serverVersion < 6:
            logger.warning(NO_DEPTH_API)
            return

        send = self.send        
        version = 3
        data = (REQ_MKT_DEPTH,
                version,
                tickerId,
                contract.symbol,
                contract.secType,
                contract.expiry,
                contract.strike,
                contract.right)
        map(send, data)

        if serverVersion >= 15:
            send(contract.multiplier)

        data = (contract.exchange,
                contract.currency,
                contract.localSymbol)
        map(send, data)

        if serverVersion >= 19:
            send(numRows)


    def cancelMktData(self, tickerId):
        """ cancelMktData(tickerId) -> cancel market data

        """
        version = 1
        map(self.send, (CANCEL_MKT_DATA, version, tickerId))


    def cancelMktDepth(self, tickerId):
        """ cancelMktDepth(tickerId) -> cancel market depth

        """
        if self.serverVersion < 6:
            logger.warning(NO_DEPTH_API)                      
            return
        
        version = 1
        map(self.send, (CANCEL_MKT_DEPTH, version, tickerId))


    def exerciseOptions(self, tickerId, contract, exerciseAction,
                        exerciseQuantity, account, override):
        """ exerciseOptions(...) -> exercise options

        """
        if self.serverVersion < 21:
            logger.error(NO_OPTION_EX_API)
            return
        version = 1
        map(self.send, (EXERCISE_OPTIONS,
                        version,
                        tickerId,
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


    def placeOrder(self, orderId, contract, order):
        """ placeOrder(orderId, contract, order) -> place an order

        """
        serverVersion = self.serverVersion
        send = self.send
        version = 20

        map(send, (PLACE_ORDER,
                   version,
                   orderId))

        ## contract fields
        map(send, (contract.symbol,
                   contract.secType,
                   contract.expiry,
                   contract.strike,
                   contract.right))
        if serverVersion >= 15:
            send(contract.multiplier)
        send(contract.exchange)
        if serverVersion >= 14:
            send(contract.primaryExch)
        send(contract.currency)
        if serverVersion >= 2:
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

        if serverVersion >= 4:
            send(order.parentId)

        ## more extended order fields
        if serverVersion >= 5:
            map(send, (order.blockOrder,
                       order.sweepToFill,
                       order.displaySize,
                       order.triggerMethod,
                       order.ignoreRth))

        if serverVersion >= 7:
            send(order.hidden)

        self.sendComboLegs(contract)

        if serverVersion >= 9:
            send(order.sharesAllocation)
            
        if serverVersion >= 10:
            send(order.discretionaryAmt)

        if serverVersion >= 11:
            send(order.goodAfterTime)

        if serverVersion >= 12:
            send(order.goodTillDate)

        if serverVersion >= 13:
            map(send, (order.faGroup,
                       order.faMethod,
                       order.faPercentage,
                       order.faProfile))

        # institutional short sale slot fields.
        if serverVersion >= 18:  
            map(send, (order.shortSaleSlot,         # 0 only for retail, 1 or 2 only for institution.
                       order.designatedLocation))   # only populate when order.shortSaleSlot = 2

        if serverVersion >= 19:
            map(send, (order.ocaType,
                       order.rthOnly,
                       order.rule80A,
                       order.settlingFirm,
                       order.allOrNone))
            map(send, (order.minQty, order.percentOffset,))
            map(send, (order.eTradeOnly, order.firmQuoteOnly,))
            map(send, (order.nbboPriceCap, order.auctionStrategy, 
                          order.startingPrice, order.stockRefPrice,
                          order.delta))
            if serverVersion == 26:
                if order.orderType == 'VOL':
                    lower = order.stockRangeLower
                    upper = order.stockRangeUpper
                else:
                    upper = lower = ''
                map(send (upper, lower))
        
        if serverVersion >= 22:
            send(order.overridePercentageConstraints)

        if serverVersion >= 26:
            map(send, (order.volatility, order.volatilityType))
            if serverVersion < 28:
                send(order.deltaNeutralOrderType == 'MKT' and 1)
            else:
                send(order.deltaNeutralOrderType)
                send(order.deltaNeutralAuxPrice)
            send(order.continuousUpdate)
            if serverVersion == 26:
                map(send, (upper, lower))
            send(order.referencePriceType)


    def reqAccountUpdates(self, subscribe=1, acctCode=''):
        """ reqAccountUpdates() -> request account data updates

        """
        send = self.send
        version = 2

        map(send, (REQ_ACCOUNT_DATA, version, subscribe))
        if self.serverVersion >= 9:
            send(acctCode)


    def reqExecutions(self, executionFilter=None):
        """ reqExecutions() -> request order execution data

        """
        send = self.send
        version = 2

        map(send, (REQ_EXECUTIONS, 
                   version))

        if self.serverVersion >= 9:
            if executionFilter is None:
                executionFilter = ib.types.ExecutionFilter()

            map(send, (executionFilter.clientId,
                       executionFilter.acctCode,
                       executionFilter.time,
                       executionFilter.symbol,
                       executionFilter.secType,
                       executionFilter.exchange,
                       executionFilter.side))


    def cancelOrder(self, orderId):
        """ cancelOrder(orderId) -> cancel order specified by orderId

        """
        version = 1
        map(self.send, (CANCEL_ORDER, version, orderId))


    def reqOpenOrders(self):
        """ reqOpenOrders() -> request order data

        """
        version = 1
        map(self.send, (REQ_OPEN_ORDERS, version))


    def reqIds(self, numIds):
        """ reqIds() -> request ids

        """
        version = 1
        map(self.send, (REQ_IDS, version, numIds))


    def reqNewsBulletins(self, all=True):
        """ reqNewsBulletins(all=True) -> request news bulletin updates

        """
        version = 1
        map(self.send, (REQ_NEWS_BULLETINS, version, int(all)))


    def cancelNewsBulletins(self):
        """ cancelNewsBulletins() -> cancel news bulletin updates

        """
        version = 1
        map(self.send, (CANCEL_NEWS_BULLETINS, version))


    def setServerLogLevel(self, logLevel):
        """ setServerLogLevel(logLevel=[1..4]) -> set the server log verbosity

        """
        version = 1
        map(self.send, (SET_SERVER_LOGLEVEL, version, logLevel))


    def reqAutoOpenOrders(self, autoBind=True):
        """ reqAutoOpenOrders() -> request auto open orders

        """
        version = 1
        map(self.send, (REQ_AUTO_OPEN_ORDERS, version, int(autoBind)))


    def reqAllOpenOrders(self):
        """ reqAllOpenOrders() -> request all open orders

        """
        version = 1
        map(self.send, (REQ_ALL_OPEN_ORDERS, version))


    def reqManagedAccts(self):
        """ reqManagedAccts() -> request managed accounts

        """
        version = 1
        map(self.send, (REQ_MANAGED_ACCTS, version))


    def requestFA(self, faDataType):
        """ requestFA(faDataType) -> request fa of some type

        """
        if self.serverVersion < 13:
            logger.error(NO_FA_API)
            return

        version = 1
        map(self.send, (REQ_FA, version, faDataType))


    def replaceFA(self, faDataType, xml):
        """ replaceFA(faDataType, xml) -> replace fa

        """
        if self.serverVersion < 13:
            logger.error(NO_FA_API)
            return

        version = 1
        map(self.send, (REPLACE_FA, version, faDataType, xml))


    def send(self, data, packfunc=struct.pack):
        """ send(data) -> send a value to TWS

        """
        sendfunc = self.socket.send
        for k in str(data):
            sendfunc(packfunc('!i', ord(k))[3])
        sendfunc(EOF)


    def sendComboLegs(self, contract):
        """ sendComboLegs(contract) -> helper to send a contracts combo legs

        """
        send = self.send

        if self.serverVersion >= 8 and contract.secType.lower() == BAG_SEC_TYPE:
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


    def register(self, messageType, listener):
        """ register(listener) -> add callable listener to message receivers

        """
        for reader in self.readers.values():
            if isinstance(reader , (messageType, )):
                if not reader.listeners.count(listener):
                    reader.listeners.append(listener)


    def deregister(self, messageType, listener):
        """ deregister(listener) -> remove listener from message receivers

        """
        for reader in self.readers.values():
            if isinstance(reader, (messageType, )):
                try:
                    reader.listeners.remove(listener)
                except (ValueError, ):
                    pass


def build(clientId=0, reader=None):
    """ build(clientId) -> creates a new ib socket connection

    """
    if reader is None:
        reader = SocketReader
    return SocketConnection(clientId=clientId, reader=reader)
