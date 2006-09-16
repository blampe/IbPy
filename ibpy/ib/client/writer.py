#!/usr/bin/env python
""" ib.client.writer -> IB TWS socket connection and message encoder.

"""
from socket import socket, AF_INET, SOCK_STREAM
from struct import pack

from ib import lib
from ib.client import message
from ib.types import ExecutionFilter


CLIENT_VERSION = 27
SERVER_VERSION = 1
EOL = pack('!i', 0)[3]
BAG_SEC_TYPE = 'BAG'

## fa message data types
GROUPS, PROFILES, ALIASES = range(1, 4)

## outgoing message ids
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

## incoming message ids.  reader start and stop message ids are local
## to this package.
READER_START, READER_STOP = -2, -1

(
TICK_PRICE, TICK_SIZE, ORDER_STATUS, ERR_MSG, OPEN_ORDER, ACCT_VALUE,
PORTFOLIO_VALUE, ACCT_UPDATE_TIME, NEXT_VALID_ID, CONTRACT_DATA,
EXECUTION_DATA, MARKET_DEPTH, MARKET_DEPTH_L2, NEWS_BULLETINS,
MANAGED_ACCTS, RECEIVE_FA, HISTORICAL_DATA, BOND_CONTRACT_DATA,
SCANNER_PARAMETERS, SCANNER_DATA, TICK_OPTION_COMPUTATION,
) = range(1, 22)

## local error strings
NO_API_FMT = 'Connected TWS version does not support %s API.'
NO_SCANNER_API = NO_API_FMT % 'scanner'
NO_CONTRACT_API = NO_API_FMT % 'contract details'
NO_DEPTH_API = NO_API_FMT % 'market depth'
NO_OPTION_EX_API = NO_API_FMT % 'options exercise'
NO_FA_API = NO_API_FMT % 'fa'

## local logger
logger = lib.logger()


class ConnectedWriter(object):
    """ ConnectedWriter(...) -> useful wrapper of a socket for IB

    This type defines methods for requesting ticker data, account data, etc.

    When called to connect, this type constructs a python socket, connects 
    it to TWS, and if successful, creates and starts a reader object.  The
    reader object is then responsible for slurping data from the connection 
    and doing something with it.
    """
    readerTypes = {
        ACCT_VALUE : message.AccountValue,
        ACCT_UPDATE_TIME : message.AccountTime,
        CONTRACT_DATA : message.ContractDetails,
        ERR_MSG : message.Error,
        EXECUTION_DATA : message.Execution,
        RECEIVE_FA : message.ReceiveFa,
        MANAGED_ACCTS : message.ManagedAccounts,
        MARKET_DEPTH : message.MarketDepth,
        MARKET_DEPTH_L2 : message.MarketDepthLevel2,
        NEWS_BULLETINS : message.NewsBulletin,
        NEXT_VALID_ID : message.NextId,
        OPEN_ORDER : message.OpenOrder,
        ORDER_STATUS : message.OrderStatus,
        PORTFOLIO_VALUE : message.Portfolio,
        READER_START : message.ReaderStart,
        READER_STOP : message.ReaderStop,
        TICK_PRICE : message.TickPrice,
        TICK_SIZE : message.TickSize,
        HISTORICAL_DATA : message.HistoricalData,
        BOND_CONTRACT_DATA : message.BondContractData,
        SCANNER_PARAMETERS : message.ScannerParameters,
        SCANNER_DATA : message.ScannerData,
        TICK_OPTION_COMPUTATION : message.TickOptionComputation,
    }


    def __init__(self, clientId, readerType):
        self.clientId = clientId
        self.serverVersion = 0
        self.readerType = readerType
        decoderItems = self.readerTypes.items()
        self.decoders = dict([(id, rdr()) for id, rdr in decoderItems])
        ## this enables the ticker price message handler to call our
        ## tick size handlder.
        self.decoders[TICK_PRICE].sizer = self.decoders[TICK_SIZE]


    def connect(self, address, client_version=CLIENT_VERSION):
        """ connect((host, port)) -> construct a socket and connect it to TWS
        
        """
        debug = logger.debug
        debug('Creating socket object for %s', self)
        self.socket = socket(AF_INET, SOCK_STREAM)

        debug('Creating reader of type %s for %s', self.readerType, self)
        self.reader = self.readerType(self.decoders, self.socket)

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
        send = self.send
        sendMax = self.sendMax
        
        send(REQ_SCANNER_SUBSCRIPTION)
        send(version)
        send(tickerId)
        sendMax(subscription.numberOfRows)
        send(subscription.instrument)
        send(subscription.locationCode)
        send(subscription.scanCode)
        sendMax(subscription.abovePrice)
        sendMax(subscription.belowPrice)
        sendMax(subscription.aboveVolume)
        sendMax(subscription.marketCapAbove)
        sendMax(subscription.marketCapBelow)
        send(subscription.moodyRatingAbove)
        send(subscription.moodyRatingBelow)
        send(subscription.spRatingAbove)
        send(subscription.spRatingBelow)
        send(subscription.maturityDateAbove)
        send(subscription.maturityDateBelow)
        sendMax(subscription.couponRateAbove)
        sendMax(subscription.couponRateBelow)
        send(subscription.excludeConvertible)

        if self.serverVersion >= 25:
            send(subscription.averageOptionVolumeAbove)
            send(subscription.scannerSetttingPairs)
        if self.serverVersion >= 27:
            send(subscription.stockTypeFilter)


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

        self.sendComboLegs(contract, openClose=False)
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
        print '!!!!!!!!!'        
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
        self.sendComboLegs(contract, openClose=False)


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

    # @onlyConnected
    # @requireServerVersion

    def placeOrder(self, orderId, contract, order):
        """ placeOrder(orderId, contract, order) -> place an order

        """
        print '#####'
        serverVersion = self.serverVersion
        send = self.send
        sendMax = self.sendMax
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
        if serverVersion >= 5:
            map(send, (order.blockOrder,
                       order.sweepToFill,
                       order.displaySize,
                       order.triggerMethod,
                       order.ignoreRth))
        if serverVersion >= 7:
            send(order.hidden)

        self.sendComboLegs(contract, openClose=True)

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
        if serverVersion >= 18:  
            map(send, (order.shortSaleSlot,         # 0 only for retail, 1 or 2 only for institution.
                       order.designatedLocation))   # only populate when order.shortSaleSlot = 2

        isVol = order.orderType.upper() == 'VOL'
        
        if serverVersion >= 19:
           send(order.ocaType)
           send(order.rthOnly)
           send(order.rule80A)
           send(order.settlingFirm)
           send(order.allOrNone)
           sendMax(order.minQty)
           sendMax(order.percentOffset)
           send(order.eTradeOnly)
           send(order.firmQuoteOnly)
           sendMax(order.nbboPriceCap)
           sendMax(order.auctionStrategy)
           sendMax(order.startingPrice)
           sendMax(order.stockRefPrice)
           sendMax(order.delta)

           if isVol and serverVersion == 26:
               upper = lower = lib.maxfloat
           else:
               lower = order.stockRangeLower
               upper = order.stockRangeUpper
           map(sendMax, (upper, lower))
        
        if serverVersion >= 22:
            send(order.overridePercentageConstraints)

        if serverVersion >= 26:
            map(sendMax, (order.volatility,
                          order.volatilityType))
            if serverVersion < 28:
                send(int(order.deltaNeutralOrderType.upper() == 'MKT'))
            else:
                send(order.deltaNeutralOrderType)
                sendMax(order.deltaNeutralAuxPrice)
            send(order.continuousUpdate)
            if serverVersion == 26:
                if isVol:
                   lower = order.stockRangeLower
                   upper = order.stockRangeUpper                   
                else:
                   upper = lower = maxfloat
                map(sendMax, (upper, lower))
            sendMax(order.referencePriceType)


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
                executionFilter = ExecutionFilter()

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


    def send(self, data, packfunc=pack, eol=EOL):
        """ send(data) -> send a value to TWS

        """
        print '***', data
        sendfunc = self.socket.send
        for k in str(data):
            sendfunc(packfunc('!i', ord(k))[3])
        sendfunc(eol)


    def sendMax(self, data, eol=EOL, maxes=(lib.maxint, lib.maxfloat)):
        """ send(data) -> send a value to TWS, changing some values

        """
        if data in maxes:
            self.socket.send(eol)
        else:
            self.send(data)


    def sendComboLegs(self, contract, openClose):
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
                               leg.exchange))
                    if openClose:
                        send(leg.openClose)
            else:
                send(0)


    def register(self, messageType, listener):
        """ register(listener) -> add callable listener to message receivers

        """
        for decoder in self.decoders.values():
            if isinstance(decoder , (messageType, )):
                if not decoder.listeners.count(listener):
                    decoder.listeners.append(listener)


    def deregister(self, messageType, listener):
        """ deregister(listener) -> remove listener from message receivers

        """
        for decoder in self.decoders.values():
            if isinstance(decoder, (messageType, )):
                try:
                    decoder.listeners.remove(listener)
                except (ValueError, ):
                    pass



