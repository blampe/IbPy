#!/usr/bin/env python
""" ib.client.writer -> IB TWS socket connection and message encoder.

"""
from operator import lt, gt
from struct import pack
from sys import _getframe

from ib import lib
from ib.client import message, support
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

## local error strings
NO_API_FMT = 'Connected TWS version does not support %s API.'
NO_SCANNER_API = NO_API_FMT % 'scanner'
NO_CONTRACT_API = NO_API_FMT % 'contract details'
NO_DEPTH_API = NO_API_FMT % 'market depth'
NO_OPTION_EX_API = NO_API_FMT % 'options exercise'
NO_FA_API = NO_API_FMT % 'fa'

logger = lib.logger()


class DefaultWriter(lib.ListenerContainer):

    def __init__(self, preListeners=None, postListeners=None,
                 serverVersion=None):
        lib.ListenerContainer.__init__(self, preListeners, postListeners)
        self.serverVersion = serverVersion


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 24, NO_SCANNER_API)
    @support.notifyEnclosure(CANCEL_SCANNER_SUBSCRIPTION)
    def cancelScannerSubscription(self, tickerId):
        """ cancelScannerSubscription(tickerId) -> cancel scanner subscription

        """
        version = 1
        map(self.send, (CANCEL_SCANNER_SUBSCRIPTION, version, tickerId))


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 24, NO_SCANNER_API)    
    @support.notifyEnclosure(REQ_SCANNER_PARAMETERS)
    def reqScannerParameters(self):
        """ reqScannerParameters() -> request scanner parameters

        """
        version = 1
        map(self.send, (REQ_SCANNER_PARAMETERS, version))


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 24, NO_SCANNER_API)    
    @support.notifyEnclosure(REQ_SCANNER_SUBSCRIPTION)
    def reqScannerSubscription(self, tickerId, subscription):
        """ reqScannerSubscription(subscription) -> request scanner subscription

        """
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


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_MKT_DATA)
    def reqMktData(self, tickerId, contract):
        """ reqMktData(tickerId, contract) -> request market data

        The tickerId value will be used by the broker to refer to the
        market instrument in subsequent communication.
        """
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


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 24, NO_SCANNER_API)    
    @support.notifyEnclosure(CANCEL_HISTORICAL_DATA)
    def cancelHistoricalData(self, tickerId):
        """ cancelHistoricalData(tickerId) ->

        """
        version = 1
        map(self.send, (CANCEL_HISTORICAL_DATA, version, tickerId))


    @support.allowOnlyConnected
    @support.restrictServerVersion(gt, 16, 'Server version mismatch.')
    @support.notifyEnclosure(REQ_HISTORICAL_DATA)
    def reqHistoricalData(self, tickerId, contract, endDateTime,
                         durationStr, barSizeSetting, whatToShow,
                         useRTH, formatDate):
        """ reqHistoricalData(...) -> request historical data

        """
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


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 4, NO_CONTRACT_API)
    @support.notifyEnclosure(REQ_CONTRACT_DATA)
    def reqContractDetails(self, contract):
        """ reqContractDetails(contract) -> request contract details

        """
        serverVersion = self.serverVersion
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


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 6, NO_DEPTH_API)
    @support.notifyEnclosure(REQ_MKT_DEPTH)
    def reqMktDepth(self, tickerId, contract, numRows=1):
        """ reqMktDepth(tickerId, contract) -> request market depth

        """
        serverVersion = self.serverVersion
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


    @support.allowOnlyConnected
    @support.notifyEnclosure(CANCEL_MKT_DATA)
    def cancelMktData(self, tickerId):
        """ cancelMktData(tickerId) -> cancel market data

        """
        version = 1
        map(self.send, (CANCEL_MKT_DATA, version, tickerId))


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 6, NO_DEPTH_API)
    @support.notifyEnclosure(CANCEL_MKT_DEPTH)
    def cancelMktDepth(self, tickerId):
        """ cancelMktDepth(tickerId) -> cancel market depth

        """
        version = 1
        map(self.send, (CANCEL_MKT_DEPTH, version, tickerId))


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 21, NO_OPTION_EX_API)
    @support.notifyEnclosure(EXERCISE_OPTIONS)
    def exerciseOptions(self, tickerId, contract, exerciseAction,
                        exerciseQuantity, account, override):
        """ exerciseOptions(...) -> exercise options

        """
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


    @support.allowOnlyConnected
    @support.notifyEnclosure(PLACE_ORDER)
    def placeOrder(self, orderId, contract, order):
        """ placeOrder(orderId, contract, order) -> place an order

        """
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


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_ACCOUNT_DATA)
    def reqAccountUpdates(self, subscribe=1, acctCode=''):
        """ reqAccountUpdates() -> request account data updates

        """
        send = self.send
        version = 2

        map(send, (REQ_ACCOUNT_DATA, version, subscribe))
        if self.serverVersion >= 9:
            send(acctCode)


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_EXECUTIONS)
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


    @support.allowOnlyConnected
    @support.notifyEnclosure(CANCEL_ORDER)
    def cancelOrder(self, orderId):
        """ cancelOrder(orderId) -> cancel order specified by orderId

        """
        version = 1
        map(self.send, (CANCEL_ORDER, version, orderId))


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_OPEN_ORDERS)
    def reqOpenOrders(self):
        """ reqOpenOrders() -> request order data

        """
        version = 1
        map(self.send, (REQ_OPEN_ORDERS, version))


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_IDS)
    def reqIds(self, numIds):
        """ reqIds() -> request ids

        """
        version = 1
        map(self.send, (REQ_IDS, version, numIds))


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_NEWS_BULLETINS)
    def reqNewsBulletins(self, all=True):
        """ reqNewsBulletins(all=True) -> request news bulletin updates

        """
        version = 1
        map(self.send, (REQ_NEWS_BULLETINS, version, int(all)))


    @support.allowOnlyConnected
    @support.notifyEnclosure(CANCEL_NEWS_BULLETINS)
    def cancelNewsBulletins(self):
        """ cancelNewsBulletins() -> cancel news bulletin updates

        """
        version = 1
        map(self.send, (CANCEL_NEWS_BULLETINS, version))


    @support.allowOnlyConnected
    @support.notifyEnclosure(SET_SERVER_LOGLEVEL)
    def setServerLogLevel(self, logLevel):
        """ setServerLogLevel(logLevel=[1..4]) -> set the server log verbosity

        """
        version = 1
        map(self.send, (SET_SERVER_LOGLEVEL, version, logLevel))


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_AUTO_OPEN_ORDERS)
    def reqAutoOpenOrders(self, autoBind=True):
        """ reqAutoOpenOrders() -> request auto open orders

        """
        version = 1
        map(self.send, (REQ_AUTO_OPEN_ORDERS, version, int(autoBind)))


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_ALL_OPEN_ORDERS)
    def reqAllOpenOrders(self):
        """ reqAllOpenOrders() -> request all open orders

        """
        version = 1
        map(self.send, (REQ_ALL_OPEN_ORDERS, version))


    @support.allowOnlyConnected
    @support.notifyEnclosure(REQ_MANAGED_ACCTS)
    def reqManagedAccts(self):
        """ reqManagedAccts() -> request managed accounts

        """
        version = 1
        map(self.send, (REQ_MANAGED_ACCTS, version))


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 13, NO_FA_API)
    @support.notifyEnclosure(REQ_FA)
    def requestFA(self, faDataType):
        """ requestFA(faDataType) -> request fa of some type

        """
        version = 1
        map(self.send, (REQ_FA, version, faDataType))


    @support.allowOnlyConnected
    @support.restrictServerVersion(lt, 13, NO_FA_API)    
    @support.notifyEnclosure(REPLACE_FA)
    def replaceFA(self, faDataType, xml):
        """ replaceFA(faDataType, xml) -> replace fa

        """
        version = 1
        map(self.send, (REPLACE_FA, version, faDataType, xml))


    def send(self, data, packfunc=pack, eol=EOL):
        """ send(data) -> send a value to TWS

        """
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

        if self.serverVersion >= 8 and contract.secType.upper() == BAG_SEC_TYPE:
            if not contract.comboLegs:
                send(0)
            else:
                send(len(contract.comboLegs))
                for leg in contract.comboLegs:
                    map(send, (leg.conId,
                               leg.ratio,
                               leg.action,
                               leg.exchange))
                    if openClose:
                        send(leg.openClose)


    def preDispatch(self, messageId):
        print '#' * 50
        print _getframe(1).f_locals
        print '#' * 50


    def postDispatch(self, messageId):
        print '*' * 50
        print _getframe(1).f_locals
        print '*' * 50
