#!/usr/bin/env python
""" generated source for module EClientSocket """
from threading import RLock

_locks = {}
def lock_for_object(obj, locks=_locks):
    return locks.setdefault(id(obj), RLock())


def synchronized(call):
    def inner(*args, **kwds):
        with lock_for_object(call):
            return call(*args, **kwds)
    return inner

#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.ext.EClientErrors import EClientErrors
from ib.ext.EReader import EReader
from ib.ext.Util import Util

from ib.lib.overloading import overloaded
from ib.lib import synchronized, Socket, DataInputStream, DataOutputStream
from ib.lib import Double, Integer

from threading import RLock
mlock = RLock()
# 
#  * EClientSocket.java
#  *
#  
# package: com.ib.client

class EClientSocket(object):
    """ generated source for class EClientSocket """
    #  Client version history
    #
    #   6 = Added parentId to orderStatus
    #   7 = The new execDetails event returned for an order filled status and reqExecDetails
    #       Also market depth is available.
    #   8 = Added lastFillPrice to orderStatus() event and permId to execution details
    #   9 = Added 'averageCost', 'unrealizedPNL', and 'unrealizedPNL' to updatePortfolio event
    #  10 = Added 'serverId' to the 'open order' & 'order status' events.
    #       We send back all the API open orders upon connection.
    #       Added new methods reqAllOpenOrders, reqAutoOpenOrders()
    #       Added FA support - reqExecution has filter.
    #                        - reqAccountUpdates takes acct code.
    #  11 = Added permId to openOrder event.
    #  12 = requsting open order attributes ignoreRth, hidden, and discretionary
    #  13 = added goodAfterTime
    #  14 = always send size on bid/ask/last tick
    #  15 = send allocation description string on openOrder
    #  16 = can receive account name in account and portfolio updates, and fa params in openOrder
    #  17 = can receive liquidation field in exec reports, and notAutoAvailable field in mkt data
    #  18 = can receive good till date field in open order messages, and request intraday backfill
    #  19 = can receive rthOnly flag in ORDER_STATUS
    #  20 = expects TWS time string on connection after server version >= 20.
    #  21 = can receive bond contract details.
    #  22 = can receive price magnifier in version 2 contract details message
    #  23 = support for scanner
    #  24 = can receive volatility order parameters in open order messages
    #  25 = can receive HMDS query start and end times
    #  26 = can receive option vols in option market data messages
    #  27 = can receive delta neutral order type and delta neutral aux price in place order version 20: API 8.85
    #  28 = can receive option model computation ticks: API 8.9
    #  29 = can receive trail stop limit price in open order and can place them: API 8.91
    #  30 = can receive extended bond contract def, new ticks, and trade count in bars
    #  31 = can receive EFP extensions to scanner and market data, and combo legs on open orders
    #     ; can receive RT bars 
    #  32 = can receive TickType.LAST_TIMESTAMP
    #     ; can receive "whyHeld" in order status messages 
    #  33 = can receive ScaleNumComponents and ScaleComponentSize is open order messages 
    #  34 = can receive whatIf orders / order state
    #  35 = can receive contId field for Contract objects
    #  36 = can receive outsideRth field for Order objects
    #  37 = can receive clearingAccount and clearingIntent for Order objects
    #  38 = can receive multiplier and primaryExchange in portfolio updates
    #     ; can receive cumQty and avgPrice in execution
    #     ; can receive fundamental data
    #     ; can receive underComp for Contract objects
    #     ; can receive reqId and end marker in contractDetails/bondContractDetails
    #     ; can receive ScaleInitComponentSize and ScaleSubsComponentSize for Order objects
    #  39 = can receive underConId in contractDetails
    #  40 = can receive algoStrategy/algoParams in openOrder
    #  41 = can receive end marker for openOrder
    #     ; can receive end marker for account download
    #     ; can receive end marker for executions download
    #  42 = can receive deltaNeutralValidation
    #  43 = can receive longName(companyName)
    #     ; can receive listingExchange
    #     ; can receive RTVolume tick
    #  44 = can receive end market for ticker snapshot
    #  45 = can receive notHeld field in openOrder
    #  46 = can receive contractMonth, industry, category, subcategory fields in contractDetails
    #     ; can receive timeZoneId, tradingHours, liquidHours fields in contractDetails
    #  47 = can receive gamma, vega, theta, undPrice fields in TICK_OPTION_COMPUTATION
    #  48 = can receive exemptCode in openOrder
    #  49 = can receive hedgeType and hedgeParam in openOrder
    #  50 = can receive optOutSmartRouting field in openOrder
    #  51 = can receive smartComboRoutingParams in openOrder
    #  52 = can receive deltaNeutralConId, deltaNeutralSettlingFirm, deltaNeutralClearingAccount and deltaNeutralClearingIntent in openOrder
    #  53 = can receive orderRef in execution
    #  54 = can receive scale order fields (PriceAdjustValue, PriceAdjustInterval, ProfitOffset, AutoReset, 
    #       InitPosition, InitFillQty and RandomPercent) in openOrder
    #  55 = can receive orderComboLegs (price) in openOrder
    #  56 = can receive trailingPercent in openOrder
    #  57 = can receive commissionReport message
    #  58 = can receive CUSIP/ISIN/etc. in contractDescription/bondContractDescription
    #  59 = can receive evRule, evMultiplier in contractDescription/bondContractDescription/executionDetails
    #       can receive multiplier in executionDetails
    #  60 = can receive deltaNeutralOpenClose, deltaNeutralShortSale, deltaNeutralShortSaleSlot and deltaNeutralDesignatedLocation in openOrder
    #  61 = can receive multiplier in openOrder
    #       can receive tradingClass in openOrder, updatePortfolio, execDetails and position
    #  62 = can receive avgCost in position message

    CLIENT_VERSION = 62
    SERVER_VERSION = 38
    EOL = 0
    BAG_SEC_TYPE = "BAG"

    #  FA msg data types
    GROUPS = 1
    PROFILES = 2
    ALIASES = 3

    @classmethod
    def faMsgTypeName(cls, faDataType):
        """ generated source for method faMsgTypeName """
        if faDataType == cls.GROUPS:
            return "GROUPS"
        elif faDataType == cls.PROFILES:
            return "PROFILES"
        elif faDataType == cls.ALIASES:
            return "ALIASES"
        return None

    #  outgoing msg id's
    REQ_MKT_DATA = 1
    CANCEL_MKT_DATA = 2
    PLACE_ORDER = 3
    CANCEL_ORDER = 4
    REQ_OPEN_ORDERS = 5
    REQ_ACCOUNT_DATA = 6
    REQ_EXECUTIONS = 7
    REQ_IDS = 8
    REQ_CONTRACT_DATA = 9
    REQ_MKT_DEPTH = 10
    CANCEL_MKT_DEPTH = 11
    REQ_NEWS_BULLETINS = 12
    CANCEL_NEWS_BULLETINS = 13
    SET_SERVER_LOGLEVEL = 14
    REQ_AUTO_OPEN_ORDERS = 15
    REQ_ALL_OPEN_ORDERS = 16
    REQ_MANAGED_ACCTS = 17
    REQ_FA = 18
    REPLACE_FA = 19
    REQ_HISTORICAL_DATA = 20
    EXERCISE_OPTIONS = 21
    REQ_SCANNER_SUBSCRIPTION = 22
    CANCEL_SCANNER_SUBSCRIPTION = 23
    REQ_SCANNER_PARAMETERS = 24
    CANCEL_HISTORICAL_DATA = 25
    REQ_CURRENT_TIME = 49
    REQ_REAL_TIME_BARS = 50
    CANCEL_REAL_TIME_BARS = 51
    REQ_FUNDAMENTAL_DATA = 52
    CANCEL_FUNDAMENTAL_DATA = 53
    REQ_CALC_IMPLIED_VOLAT = 54
    REQ_CALC_OPTION_PRICE = 55
    CANCEL_CALC_IMPLIED_VOLAT = 56
    CANCEL_CALC_OPTION_PRICE = 57
    REQ_GLOBAL_CANCEL = 58
    REQ_MARKET_DATA_TYPE = 59
    REQ_POSITIONS = 61
    REQ_ACCOUNT_SUMMARY = 62
    CANCEL_ACCOUNT_SUMMARY = 63
    CANCEL_POSITIONS = 64
    MIN_SERVER_VER_REAL_TIME_BARS = 34
    MIN_SERVER_VER_SCALE_ORDERS = 35
    MIN_SERVER_VER_SNAPSHOT_MKT_DATA = 35
    MIN_SERVER_VER_SSHORT_COMBO_LEGS = 35
    MIN_SERVER_VER_WHAT_IF_ORDERS = 36
    MIN_SERVER_VER_CONTRACT_CONID = 37
    MIN_SERVER_VER_PTA_ORDERS = 39
    MIN_SERVER_VER_FUNDAMENTAL_DATA = 40
    MIN_SERVER_VER_UNDER_COMP = 40
    MIN_SERVER_VER_CONTRACT_DATA_CHAIN = 40
    MIN_SERVER_VER_SCALE_ORDERS2 = 40
    MIN_SERVER_VER_ALGO_ORDERS = 41
    MIN_SERVER_VER_EXECUTION_DATA_CHAIN = 42
    MIN_SERVER_VER_NOT_HELD = 44
    MIN_SERVER_VER_SEC_ID_TYPE = 45
    MIN_SERVER_VER_PLACE_ORDER_CONID = 46
    MIN_SERVER_VER_REQ_MKT_DATA_CONID = 47
    MIN_SERVER_VER_REQ_CALC_IMPLIED_VOLAT = 49
    MIN_SERVER_VER_REQ_CALC_OPTION_PRICE = 50
    MIN_SERVER_VER_CANCEL_CALC_IMPLIED_VOLAT = 50
    MIN_SERVER_VER_CANCEL_CALC_OPTION_PRICE = 50
    MIN_SERVER_VER_SSHORTX_OLD = 51
    MIN_SERVER_VER_SSHORTX = 52
    MIN_SERVER_VER_REQ_GLOBAL_CANCEL = 53
    MIN_SERVER_VER_HEDGE_ORDERS = 54
    MIN_SERVER_VER_REQ_MARKET_DATA_TYPE = 55
    MIN_SERVER_VER_OPT_OUT_SMART_ROUTING = 56
    MIN_SERVER_VER_SMART_COMBO_ROUTING_PARAMS = 57
    MIN_SERVER_VER_DELTA_NEUTRAL_CONID = 58
    MIN_SERVER_VER_SCALE_ORDERS3 = 60
    MIN_SERVER_VER_ORDER_COMBO_LEGS_PRICE = 61
    MIN_SERVER_VER_TRAILING_PERCENT = 62
    MIN_SERVER_VER_DELTA_NEUTRAL_OPEN_CLOSE = 66
    MIN_SERVER_VER_ACCT_SUMMARY = 67
    MIN_SERVER_VER_TRADING_CLASS = 68
    MIN_SERVER_VER_SCALE_TABLE = 69
    
    m_anyWrapper = None #  msg handler
    m_dos = None    #  the socket output stream
    m_connected = bool()    #  true if we are connected
    m_reader = None #  thread which reads msgs from socket
    m_serverVersion = 0
    m_TwsTime = ""
    m_socket = None

    def serverVersion(self):
        """ generated source for method serverVersion """
        return self.m_serverVersion

    def TwsConnectionTime(self):
        """ generated source for method TwsConnectionTime """
        return self.m_TwsTime

    def wrapper(self):
        """ generated source for method wrapper """
        return self.m_anyWrapper

    def reader(self):
        """ generated source for method reader """
        return self.m_reader

    def __init__(self, anyWrapper):
        """ generated source for method __init__ """
        self.m_anyWrapper = anyWrapper

    def isConnected(self):
        """ generated source for method isConnected """
        return self.m_connected

    @overloaded
    @synchronized(mlock)
    def eConnect(self, host, port, clientId):
        """ generated source for method eConnect """
        #  already connected?
        host = self.checkConnected(host)
        if host is None:
            return
        try:
            self.m_socket = Socket(host, port)
            self.eConnect(self.m_socket, clientId)
        except Exception as e:
            self.eDisconnect()
            self.connectionError()

    def connectionError(self):
        """ generated source for method connectionError """
        self.m_anyWrapper.error(EClientErrors.NO_VALID_ID, EClientErrors.CONNECT_FAIL.code(), EClientErrors.CONNECT_FAIL.msg())
        self.m_reader = None

    def checkConnected(self, host):
        """ generated source for method checkConnected """
        if self.m_connected:
            self.m_anyWrapper.error(EClientErrors.NO_VALID_ID, EClientErrors.ALREADY_CONNECTED.code(), EClientErrors.ALREADY_CONNECTED.msg())
            return None
        if self.isNull(host):
            host = "127.0.0.1"
        return host

    def createReader(self, socket, dis):
        """ generated source for method createReader """
        return EReader(socket, dis)

    @synchronized(mlock)
    @eConnect.register(object, Socket, int)
    def eConnect_0(self, socket, clientId):
        """ generated source for method eConnect_0 """
        #  create io streams
        self.m_dos = DataOutputStream(socket.getOutputStream())
        #  set client version
        self.send(self.CLIENT_VERSION)
        #  start reader thread
        self.m_reader = self.createReader(self, DataInputStream(socket.getInputStream()))
        #  check server version
        self.m_serverVersion = self.m_reader.readInt()
        print "Server Version: %d" % self.m_serverVersion
        if self.m_serverVersion >= 20:
            self.m_TwsTime = self.m_reader.readStr()
            print "TWS Time at connection:" + self.m_TwsTime
        if self.m_serverVersion < self.SERVER_VERSION:
            self.eDisconnect()
            self.m_anyWrapper.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        #  Send the client id
        if self.m_serverVersion >= 3:
            self.send(clientId)
        self.m_reader.start()
        #  set connected flag
        self.m_connected = True

    @synchronized(mlock)
    def eDisconnect(self):
        """ generated source for method eDisconnect """
        #  not connected?
        if self.m_dos is None:
            return
        self.m_connected = False
        self.m_serverVersion = 0
        self.m_TwsTime = ""
        self.m_dos = None
        reader = self.m_reader
        self.m_reader = None
        socket = self.m_socket
        self.m_socket = None
        try:
            #  stop reader thread
            if reader is not None:
                reader.interrupt()
        except Exception as e:
            pass
        try:
            #  close socket
            if socket is not None:
                socket.disconnect()
        except Exception as e:
            pass

    @synchronized(mlock)
    def cancelScannerSubscription(self, tickerId):
        """ generated source for method cancelScannerSubscription """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < 24:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support API scanner subscription.")
            return
        VERSION = 1
        #  send cancel mkt data msg
        try:
            self.send(self.CANCEL_SCANNER_SUBSCRIPTION)
            self.send(VERSION)
            self.send(tickerId)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANSCANNER, str(e))
            self.close()

    @synchronized(mlock)
    def reqScannerParameters(self):
        """ generated source for method reqScannerParameters """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < 24:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support API scanner subscription.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_SCANNER_PARAMETERS)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQSCANNERPARAMETERS, str(e))
            self.close()

    @synchronized(mlock)
    def reqScannerSubscription(self, tickerId, subscription):
        """ generated source for method reqScannerSubscription """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < 24:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support API scanner subscription.")
            return
        VERSION = 3
        try:
            self.send(self.REQ_SCANNER_SUBSCRIPTION)
            self.send(VERSION)
            self.send(tickerId)
            self.sendMax(subscription.numberOfRows())
            self.send(subscription.instrument())
            self.send(subscription.locationCode())
            self.send(subscription.scanCode())
            self.sendMax(subscription.abovePrice())
            self.sendMax(subscription.belowPrice())
            self.sendMax(subscription.aboveVolume())
            self.sendMax(subscription.marketCapAbove())
            self.sendMax(subscription.marketCapBelow())
            self.send(subscription.moodyRatingAbove())
            self.send(subscription.moodyRatingBelow())
            self.send(subscription.spRatingAbove())
            self.send(subscription.spRatingBelow())
            self.send(subscription.maturityDateAbove())
            self.send(subscription.maturityDateBelow())
            self.sendMax(subscription.couponRateAbove())
            self.sendMax(subscription.couponRateBelow())
            self.send(subscription.excludeConvertible())
            if self.m_serverVersion >= 25:
                self.sendMax(subscription.averageOptionVolumeAbove())
                self.send(subscription.scannerSettingPairs())
            if self.m_serverVersion >= 27:
                self.send(subscription.stockTypeFilter())
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQSCANNER, str(e))
            self.close()

    @synchronized(mlock)
    def reqMktData(self, tickerId, contract, genericTickList, snapshot):
        """ generated source for method reqMktData """
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_SNAPSHOT_MKT_DATA and snapshot:
            self.error(tickerId, EClientErrors.UPDATE_TWS, "  It does not support snapshot market data requests.")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_UNDER_COMP:
            if contract.m_underComp is not None:
                self.error(tickerId, EClientErrors.UPDATE_TWS, "  It does not support delta-neutral orders.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_REQ_MKT_DATA_CONID:
            if contract.m_conId > 0:
                self.error(tickerId, EClientErrors.UPDATE_TWS, "  It does not support conId parameter.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
            if not self.IsEmpty(contract.m_tradingClass):
                self.error(tickerId, EClientErrors.UPDATE_TWS, "  It does not support tradingClass parameter in reqMarketData.")
                return
        VERSION = 10
        try:
            #  send req mkt data msg
            self.send(self.REQ_MKT_DATA)
            self.send(VERSION)
            self.send(tickerId)
            #  send contract fields
            if self.m_serverVersion >= self.MIN_SERVER_VER_REQ_MKT_DATA_CONID:
                self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            if self.m_serverVersion >= 15:
                self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            if self.m_serverVersion >= 14:
                self.send(contract.m_primaryExch)
            self.send(contract.m_currency)
            if self.m_serverVersion >= 2:
                self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            if self.m_serverVersion >= 8 and self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                if contract.m_comboLegs is None:
                    self.send(0)
                else:
                    self.send(len(contract.m_comboLegs))
                    i = 0
                    while i < len(contract.m_comboLegs):
                        comboLeg = contract.m_comboLegs[i]
                        self.send(comboLeg.m_conId)
                        self.send(comboLeg.m_ratio)
                        self.send(comboLeg.m_action)
                        self.send(comboLeg.m_exchange)
                        i += 1
            if self.m_serverVersion >= self.MIN_SERVER_VER_UNDER_COMP:
                if contract.m_underComp is not None:
                    underComp = contract.m_underComp
                    self.send(True)
                    self.send(underComp.m_conId)
                    self.send(underComp.m_delta)
                    self.send(underComp.m_price)
                else:
                    self.send(False)
            if self.m_serverVersion >= 31:
                #
                # * Note: Even though SHORTABLE tick type supported only
                # *       starting server version 33 it would be relatively
                # *       expensive to expose this restriction here.
                # *
                # *       Therefore we are relying on TWS doing validation.
                #
                self.send(genericTickList)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SNAPSHOT_MKT_DATA:
                self.send(snapshot)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQMKT, str(e))
            self.close()

    @synchronized(mlock)
    def cancelHistoricalData(self, tickerId):
        """ generated source for method cancelHistoricalData """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < 24:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support historical data query cancellation.")
            return
        VERSION = 1
        #  send cancel mkt data msg
        try:
            self.send(self.CANCEL_HISTORICAL_DATA)
            self.send(VERSION)
            self.send(tickerId)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANHISTDATA, str(e))
            self.close()

    def cancelRealTimeBars(self, tickerId):
        """ generated source for method cancelRealTimeBars """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REAL_TIME_BARS:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support realtime bar data query cancellation.")
            return
        VERSION = 1
        #  send cancel mkt data msg
        try:
            self.send(self.CANCEL_REAL_TIME_BARS)
            self.send(VERSION)
            self.send(tickerId)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANRTBARS, str(e))
            self.close()

    #  Note that formatData parameter affects intra-day bars only; 1-day bars always return with date in YYYYMMDD format. 
    @synchronized(mlock)
    def reqHistoricalData(self, tickerId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate):
        """ generated source for method reqHistoricalData """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 5
        try:
            if self.m_serverVersion < 16:
                self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support historical data backfill.")
                return
            if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
                if not self.IsEmpty(contract.m_tradingClass) or (contract.m_conId > 0):
                    self.error(tickerId, EClientErrors.UPDATE_TWS, "  It does not support conId and trade parameters in reqHistroricalData.")                                                                
                    return
            self.send(self.REQ_HISTORICAL_DATA)
            self.send(VERSION)
            self.send(tickerId)
            #  send contract fields
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            self.send(contract.m_primaryExch)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            if self.m_serverVersion >= 31:
                self.send(1 if contract.m_includeExpired else 0)
            if self.m_serverVersion >= 20:
                self.send(endDateTime)
                self.send(barSizeSetting)
            self.send(durationStr)
            self.send(useRTH)
            self.send(whatToShow)
            if self.m_serverVersion > 16:
                self.send(formatDate)
            if self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                if contract.m_comboLegs is None:
                    self.send(0)
                else:
                    self.send(len(contract.m_comboLegs))
                    i = 0
                    while i < len(contract.m_comboLegs):
                        comboLeg = contract.m_comboLegs[i]
                        self.send(comboLeg.m_conId)
                        self.send(comboLeg.m_ratio)
                        self.send(comboLeg.m_action)
                        self.send(comboLeg.m_exchange)
                        i += 1
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQHISTDATA, str(e))
            self.close()

    @synchronized(mlock)
    def reqRealTimeBars(self, tickerId, contract, barSize, whatToShow, useRTH):
        """ generated source for method reqRealTimeBars """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REAL_TIME_BARS:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support real time bars.")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
            if not self.IsEmpty(contract.m_tradingClass) or (contract.m_conId > 0):
                self.error(tickerId, EClientErrors.UPDATE_TWS, "  It does not support conId and tradingClass parameters in reqRealTimeBars.")
                return
        VERSION = 2
        try:
            #  send req mkt data msg
            self.send(self.REQ_REAL_TIME_BARS)
            self.send(VERSION)
            self.send(tickerId)
            #  send contract fields
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            self.send(contract.m_primaryExch)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            self.send(barSize)
            #  this parameter is not currently used
            self.send(whatToShow)
            self.send(useRTH)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQRTBARS, str(e))
            self.close()

    @synchronized(mlock)
    def reqContractDetails(self, reqId, contract):
        """ generated source for method reqContractDetails """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        #  This feature is only available for versions of TWS >=4
        if self.m_serverVersion < 4:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_SEC_ID_TYPE:
            if not self.IsEmpty(contract.m_secIdType) or not self.IsEmpty(contract.m_secId):
                self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support secIdType and secId parameters.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
            if not self.IsEmpty(contract.m_tradingClass):
                self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support tradingClass parameter in reqContractDetails.")
                return
        VERSION = 7
        try:
            #  send req mkt data msg
            self.send(self.REQ_CONTRACT_DATA)
            self.send(VERSION)
            if self.m_serverVersion >= self.MIN_SERVER_VER_CONTRACT_DATA_CHAIN:
                self.send(reqId)
            #  send contract fields
            if self.m_serverVersion >= self.MIN_SERVER_VER_CONTRACT_CONID:
                self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            if self.m_serverVersion >= 15:
                self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            if self.m_serverVersion >= 31:
                self.send(contract.m_includeExpired)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SEC_ID_TYPE:
                self.send(contract.m_secIdType)
                self.send(contract.m_secId)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQCONTRACT, str(e))
            self.close()

    @synchronized(mlock)
    def reqMktDepth(self, tickerId, contract, numRows):
        """ generated source for method reqMktDepth """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        #  This feature is only available for versions of TWS >=6
        if self.m_serverVersion < 6:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
            if not self.IsEmpty(contract.m_tradingClass) or (contract.m_conId > 0):
                self.error(tickerId, EClientErrors.UPDATE_TWS, "  It does not support conId and tradingClass parameters in reqMktDepth.")
                return
        VERSION = 4
        try:
            #  send req mkt data msg
            self.send(self.REQ_MKT_DEPTH)
            self.send(VERSION)
            self.send(tickerId)
            #  send contract fields
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            if self.m_serverVersion >= 15:
                self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            if self.m_serverVersion >= 19:
                self.send(numRows)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQMKTDEPTH, str(e))
            self.close()

    @synchronized(mlock)
    def cancelMktData(self, tickerId):
        """ generated source for method cancelMktData """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        #  send cancel mkt data msg
        try:
            self.send(self.CANCEL_MKT_DATA)
            self.send(VERSION)
            self.send(tickerId)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANMKT, str(e))
            self.close()

    @synchronized(mlock)
    def cancelMktDepth(self, tickerId):
        """ generated source for method cancelMktDepth """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        #  This feature is only available for versions of TWS >=6
        if self.m_serverVersion < 6:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        VERSION = 1
        #  send cancel mkt data msg
        try:
            self.send(self.CANCEL_MKT_DEPTH)
            self.send(VERSION)
            self.send(tickerId)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANMKTDEPTH, str(e))
            self.close()

    @synchronized(mlock)
    def exerciseOptions(self, tickerId, contract, exerciseAction, exerciseQuantity, account, override):
        """ generated source for method exerciseOptions """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 2
        try:
            if self.m_serverVersion < 21:
                self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support options exercise from the API.")
                return
            if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
                if not self.IsEmpty(contract.m_tradingClass) or (contract.m_conId > 0):
                    self.error(tickerId, EClientErrors.UPDATE_TWS, "  It does not support conId and tradingClass parameters in exerciseOptions.")
                    return
            self.send(self.EXERCISE_OPTIONS)
            self.send(VERSION)
            self.send(tickerId)
            #  send contract fields
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            self.send(exerciseAction)
            self.send(exerciseQuantity)
            self.send(account)
            self.send(override)
        except Exception as e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQMKT, str(e))
            self.close()

    @synchronized(mlock)
    def placeOrder(self, id, contract, order):
        """ generated source for method placeOrder """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_SCALE_ORDERS:
            if (order.m_scaleInitLevelSize != Integer.MAX_VALUE) or (order.m_scalePriceIncrement != Double.MAX_VALUE):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support Scale orders.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SSHORT_COMBO_LEGS:
            if contract.m_comboLegs:
                i = 0
                while i < len(contract.m_comboLegs):
                    comboLeg = contract.m_comboLegs[i]
                    if comboLeg.m_shortSaleSlot != 0 or not self.IsEmpty(comboLeg.m_designatedLocation):
                        self.error(id, EClientErrors.UPDATE_TWS, "  It does not support SSHORT flag for combo legs.")
                        return
                    i += 1
        if self.m_serverVersion < self.MIN_SERVER_VER_WHAT_IF_ORDERS:
            if order.m_whatIf:
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support what-if orders.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_UNDER_COMP:
            if contract.m_underComp is not None:
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support delta-neutral orders.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SCALE_ORDERS2:
            if order.m_scaleSubsLevelSize != Integer.MAX_VALUE:
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support Subsequent Level Size for Scale orders.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_ALGO_ORDERS:
            if not self.IsEmpty(order.m_algoStrategy):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support algo orders.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_NOT_HELD:
            if order.m_notHeld:
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support notHeld parameter.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SEC_ID_TYPE:
            if not self.IsEmpty(contract.m_secIdType) or not self.IsEmpty(contract.m_secId):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support secIdType and secId parameters.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_PLACE_ORDER_CONID:
            if contract.m_conId > 0:
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support conId parameter.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SSHORTX:
            if order.m_exemptCode != -1:
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support exemptCode parameter.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SSHORTX:
            if contract.m_comboLegs:
                i = 0
                while i < len(contract.m_comboLegs):
                    comboLeg = contract.m_comboLegs[i]
                    if comboLeg.m_exemptCode != -1:
                        self.error(id, EClientErrors.UPDATE_TWS, "  It does not support exemptCode parameter.")
                        return
                    i += 1
        if self.m_serverVersion < self.MIN_SERVER_VER_HEDGE_ORDERS:
            if not self.IsEmpty(order.m_hedgeType):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support hedge orders.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_OPT_OUT_SMART_ROUTING:
            if order.m_optOutSmartRouting:
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support optOutSmartRouting parameter.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_DELTA_NEUTRAL_CONID:
            if order.m_deltaNeutralConId > 0 or not self.IsEmpty(order.m_deltaNeutralSettlingFirm) or not self.IsEmpty(order.m_deltaNeutralClearingAccount) or not self.IsEmpty(order.m_deltaNeutralClearingIntent):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support deltaNeutral parameters: ConId, SettlingFirm, ClearingAccount, ClearingIntent")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_DELTA_NEUTRAL_OPEN_CLOSE:
            if not self.IsEmpty(order.m_deltaNeutralOpenClose) or order.m_deltaNeutralShortSale or order.m_deltaNeutralShortSaleSlot > 0 or not self.IsEmpty(order.m_deltaNeutralDesignatedLocation):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support deltaNeutral parameters: OpenClose, ShortSale, ShortSaleSlot, DesignatedLocation")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SCALE_ORDERS3:
            if order.m_scalePriceIncrement > 0 and order.m_scalePriceIncrement != Double.MAX_VALUE:
                if order.m_scalePriceAdjustValue != Double.MAX_VALUE or order.m_scalePriceAdjustInterval != Integer.MAX_VALUE or order.m_scaleProfitOffset != Double.MAX_VALUE or order.m_scaleAutoReset or order.m_scaleInitPosition != Integer.MAX_VALUE or order.m_scaleInitFillQty != Integer.MAX_VALUE or order.m_scaleRandomPercent:
                    self.error(id, EClientErrors.UPDATE_TWS, "  It does not support Scale order parameters: PriceAdjustValue, PriceAdjustInterval, " + "ProfitOffset, AutoReset, InitPosition, InitFillQty and RandomPercent")
                    return
        if self.m_serverVersion < self.MIN_SERVER_VER_ORDER_COMBO_LEGS_PRICE and self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
            if order.m_orderComboLegs:
                i = 0
                while i < len(order.m_orderComboLegs):
                    orderComboLeg = order.m_orderComboLegs[i]
                    if orderComboLeg.m_price != Double.MAX_VALUE:
                        self.error(id, EClientErrors.UPDATE_TWS, "  It does not support per-leg prices for order combo legs.")
                        return
                    i += 1
        if self.m_serverVersion < self.MIN_SERVER_VER_TRAILING_PERCENT:
            if order.m_trailingPercent != Double.MAX_VALUE:
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support trailing percent parameter")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
            if not self.IsEmpty(contract.m_tradingClass):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support tradingClass parameters in placeOrder.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SCALE_TABLE:
            if not self.IsEmpty(order.m_scaleTable) or not self.IsEmpty(order.m_activeStartTime) or not self.IsEmpty(order.m_activeStopTime):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support scaleTable, activeStartTime and activeStopTime parameters.")
                return
        VERSION = 27 if (self.m_serverVersion < self.MIN_SERVER_VER_NOT_HELD) else 41
        #  send place order msg
        try:
            self.send(self.PLACE_ORDER)
            self.send(VERSION)
            self.send(id)
            #  send contract fields
            if self.m_serverVersion >= self.MIN_SERVER_VER_PLACE_ORDER_CONID:
                self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            if self.m_serverVersion >= 15:
                self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            if self.m_serverVersion >= 14:
                self.send(contract.m_primaryExch)
            self.send(contract.m_currency)
            if self.m_serverVersion >= 2:
                self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SEC_ID_TYPE:
                self.send(contract.m_secIdType)
                self.send(contract.m_secId)
            #  send main order fields
            self.send(order.m_action)
            self.send(order.m_totalQuantity)
            self.send(order.m_orderType)
            if self.m_serverVersion < self.MIN_SERVER_VER_ORDER_COMBO_LEGS_PRICE:
                self.send(0 if order.m_lmtPrice == Double.MAX_VALUE else order.m_lmtPrice)
            else:
                self.sendMax(order.m_lmtPrice)
            if self.m_serverVersion < self.MIN_SERVER_VER_TRAILING_PERCENT:
                self.send(0 if order.m_auxPrice == Double.MAX_VALUE else order.m_auxPrice)
            else:
                self.sendMax(order.m_auxPrice)
            #  send extended order fields
            self.send(order.m_tif)
            self.send(order.m_ocaGroup)
            self.send(order.m_account)
            self.send(order.m_openClose)
            self.send(order.m_origin)
            self.send(order.m_orderRef)
            self.send(order.m_transmit)
            if self.m_serverVersion >= 4:
                self.send(order.m_parentId)
            if self.m_serverVersion >= 5:
                self.send(order.m_blockOrder)
                self.send(order.m_sweepToFill)
                self.send(order.m_displaySize)
                self.send(order.m_triggerMethod)
                if self.m_serverVersion < 38:
                    #  will never happen
                    self.send(False)#  order.m_ignoreRth 
                else:
                    self.send(order.m_outsideRth)
            if self.m_serverVersion >= 7:
                self.send(order.m_hidden)
            #  Send combo legs for BAG requests
            if self.m_serverVersion >= 8 and self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                if contract.m_comboLegs is None:
                    self.send(0)
                else:
                    self.send(len(contract.m_comboLegs))
                    i = 0
                    while i < len(contract.m_comboLegs):
                        comboLeg = contract.m_comboLegs[i]
                        self.send(comboLeg.m_conId)
                        self.send(comboLeg.m_ratio)
                        self.send(comboLeg.m_action)
                        self.send(comboLeg.m_exchange)
                        self.send(comboLeg.m_openClose)
                        if self.m_serverVersion >= self.MIN_SERVER_VER_SSHORT_COMBO_LEGS:
                            self.send(comboLeg.m_shortSaleSlot)
                            self.send(comboLeg.m_designatedLocation)
                        if self.m_serverVersion >= self.MIN_SERVER_VER_SSHORTX_OLD:
                            self.send(comboLeg.m_exemptCode)
                        i += 1
            #  Send order combo legs for BAG requests
            if self.m_serverVersion >= self.MIN_SERVER_VER_ORDER_COMBO_LEGS_PRICE and self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                if order.m_orderComboLegs is None:
                    self.send(0)
                else:
                    self.send(len(order.m_orderComboLegs))
                    i = 0
                    while i < len(order.m_orderComboLegs):
                        orderComboLeg = order.m_orderComboLegs[i]
                        self.sendMax(orderComboLeg.m_price)
                        i += 1
            if self.m_serverVersion >= self.MIN_SERVER_VER_SMART_COMBO_ROUTING_PARAMS and self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                smartComboRoutingParams = order.m_smartComboRoutingParams
                smartComboRoutingParamsCount = 0 if smartComboRoutingParams is None else len(smartComboRoutingParams)
                self.send(smartComboRoutingParamsCount)
                if smartComboRoutingParamsCount > 0:
                    i = 0
                    while i < smartComboRoutingParamsCount:
                        tagValue = smartComboRoutingParams[i]
                        self.send(tagValue.m_tag)
                        self.send(tagValue.m_value)
                        i += 1
            if self.m_serverVersion >= 9:
                #  send deprecated sharesAllocation field
                self.send("")
            if self.m_serverVersion >= 10:
                self.send(order.m_discretionaryAmt)
            if self.m_serverVersion >= 11:
                self.send(order.m_goodAfterTime)
            if self.m_serverVersion >= 12:
                self.send(order.m_goodTillDate)
            if self.m_serverVersion >= 13:
                self.send(order.m_faGroup)
                self.send(order.m_faMethod)
                self.send(order.m_faPercentage)
                self.send(order.m_faProfile)
            if self.m_serverVersion >= 18:
                #  institutional short sale slot fields.
                self.send(order.m_shortSaleSlot)
                #  0 only for retail, 1 or 2 only for institution.
                self.send(order.m_designatedLocation)
                #  only populate when order.m_shortSaleSlot = 2.
            if self.m_serverVersion >= self.MIN_SERVER_VER_SSHORTX_OLD:
                self.send(order.m_exemptCode)
            if self.m_serverVersion >= 19:
                self.send(order.m_ocaType)
                if self.m_serverVersion < 38:
                    #  will never happen
                    self.send(False)#  order.m_rthOnly 
                self.send(order.m_rule80A)
                self.send(order.m_settlingFirm)
                self.send(order.m_allOrNone)
                self.sendMax(order.m_minQty)
                self.sendMax(order.m_percentOffset)
                self.send(order.m_eTradeOnly)
                self.send(order.m_firmQuoteOnly)
                self.sendMax(order.m_nbboPriceCap)
                self.sendMax(order.m_auctionStrategy)
                self.sendMax(order.m_startingPrice)
                self.sendMax(order.m_stockRefPrice)
                self.sendMax(order.m_delta)
                #  Volatility orders had specific watermark price attribs in server version 26
                lower = Double.MAX_VALUE if (self.m_serverVersion == 26) and order.m_orderType == "VOL" else order.m_stockRangeLower
                upper = Double.MAX_VALUE if (self.m_serverVersion == 26) and order.m_orderType == "VOL" else order.m_stockRangeUpper
                self.sendMax(lower)
                self.sendMax(upper)
            if self.m_serverVersion >= 22:
                self.send(order.m_overridePercentageConstraints)
            if self.m_serverVersion >= 26:
                #  Volatility orders
                self.sendMax(order.m_volatility)
                self.sendMax(order.m_volatilityType)
                if self.m_serverVersion < 28:
                    self.send(order.m_deltaNeutralOrderType.lower() == "MKT".lower())
                else:
                    self.send(order.m_deltaNeutralOrderType)
                    self.sendMax(order.m_deltaNeutralAuxPrice)
                    if self.m_serverVersion >= self.MIN_SERVER_VER_DELTA_NEUTRAL_CONID and not self.IsEmpty(order.m_deltaNeutralOrderType):
                        self.send(order.m_deltaNeutralConId)
                        self.send(order.m_deltaNeutralSettlingFirm)
                        self.send(order.m_deltaNeutralClearingAccount)
                        self.send(order.m_deltaNeutralClearingIntent)
                    if self.m_serverVersion >= self.MIN_SERVER_VER_DELTA_NEUTRAL_OPEN_CLOSE and not self.IsEmpty(order.m_deltaNeutralOrderType):
                        self.send(order.m_deltaNeutralOpenClose)
                        self.send(order.m_deltaNeutralShortSale)
                        self.send(order.m_deltaNeutralShortSaleSlot)
                        self.send(order.m_deltaNeutralDesignatedLocation)
                self.send(order.m_continuousUpdate)
                if self.m_serverVersion == 26:
                    #  Volatility orders had specific watermark price attribs in server version 26
                    lower = order.m_stockRangeLower if order.m_orderType == "VOL" else Double.MAX_VALUE
                    upper = order.m_stockRangeUpper if order.m_orderType == "VOL" else Double.MAX_VALUE
                    self.sendMax(lower)
                    self.sendMax(upper)
                self.sendMax(order.m_referencePriceType)
            if self.m_serverVersion >= 30:
                #  TRAIL_STOP_LIMIT stop price
                self.sendMax(order.m_trailStopPrice)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRAILING_PERCENT:
                self.sendMax(order.m_trailingPercent)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SCALE_ORDERS:
                if self.m_serverVersion >= self.MIN_SERVER_VER_SCALE_ORDERS2:
                    self.sendMax(order.m_scaleInitLevelSize)
                    self.sendMax(order.m_scaleSubsLevelSize)
                else:
                    self.send("")
                    self.sendMax(order.m_scaleInitLevelSize)
                self.sendMax(order.m_scalePriceIncrement)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SCALE_ORDERS3 and order.m_scalePriceIncrement > 0.0 and order.m_scalePriceIncrement != Double.MAX_VALUE:
                self.sendMax(order.m_scalePriceAdjustValue)
                self.sendMax(order.m_scalePriceAdjustInterval)
                self.sendMax(order.m_scaleProfitOffset)
                self.send(order.m_scaleAutoReset)
                self.sendMax(order.m_scaleInitPosition)
                self.sendMax(order.m_scaleInitFillQty)
                self.send(order.m_scaleRandomPercent)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SCALE_TABLE:
                self.send(order.m_scaleTable)
                self.send(order.m_activeStartTime)
                self.send(order.m_activeStopTime)
            if self.m_serverVersion >= self.MIN_SERVER_VER_HEDGE_ORDERS:
                self.send(order.m_hedgeType)
                if not self.IsEmpty(order.m_hedgeType):
                    self.send(order.m_hedgeParam)
            if self.m_serverVersion >= self.MIN_SERVER_VER_OPT_OUT_SMART_ROUTING:
                self.send(order.m_optOutSmartRouting)
            if self.m_serverVersion >= self.MIN_SERVER_VER_PTA_ORDERS:
                self.send(order.m_clearingAccount)
                self.send(order.m_clearingIntent)
            if self.m_serverVersion >= self.MIN_SERVER_VER_NOT_HELD:
                self.send(order.m_notHeld)
            if self.m_serverVersion >= self.MIN_SERVER_VER_UNDER_COMP:
                if contract.m_underComp is not None:
                    underComp = contract.m_underComp
                    self.send(True)
                    self.send(underComp.m_conId)
                    self.send(underComp.m_delta)
                    self.send(underComp.m_price)
                else:
                    self.send(False)
            if self.m_serverVersion >= self.MIN_SERVER_VER_ALGO_ORDERS:
                self.send(order.m_algoStrategy)
                if not self.IsEmpty(order.m_algoStrategy):
                    algoParams = order.m_algoParams
                    algoParamsCount = 0 if algoParams is None else len(algoParams)
                    self.send(algoParamsCount)
                    if algoParamsCount > 0:
                        i = 0
                        while i < algoParamsCount:
                            tagValue = algoParams[i]
                            self.send(tagValue.m_tag)
                            self.send(tagValue.m_value)
                            i += 1
            if self.m_serverVersion >= self.MIN_SERVER_VER_WHAT_IF_ORDERS:
                self.send(order.m_whatIf)
        except Exception as e:
            self.error_0(id, EClientErrors.FAIL_SEND_ORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqAccountUpdates(self, subscribe, acctCode):
        """ generated source for method reqAccountUpdates """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 2
        #  send cancel order msg
        try:
            self.send(self.REQ_ACCOUNT_DATA)
            self.send(VERSION)
            self.send(subscribe)
            #  Send the account code. This will only be used for FA clients
            if self.m_serverVersion >= 9:
                self.send(acctCode)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_ACCT, str(e))
            self.close()

    @synchronized(mlock)
    def reqExecutions(self, reqId, filter):
        """ generated source for method reqExecutions """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 3
        #  send cancel order msg
        try:
            self.send(self.REQ_EXECUTIONS)
            self.send(VERSION)
            if self.m_serverVersion >= self.MIN_SERVER_VER_EXECUTION_DATA_CHAIN:
                self.send(reqId)
            #  Send the execution rpt filter data
            if self.m_serverVersion >= 9:
                self.send(filter.m_clientId)
                self.send(filter.m_acctCode)
                #  Note that the valid format for m_time is "yyyymmdd-hh:mm:ss"
                self.send(filter.m_time)
                self.send(filter.m_symbol)
                self.send(filter.m_secType)
                self.send(filter.m_exchange)
                self.send(filter.m_side)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_EXEC, str(e))
            self.close()

    @synchronized(mlock)
    def cancelOrder(self, id):
        """ generated source for method cancelOrder """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        #  send cancel order msg
        try:
            self.send(self.CANCEL_ORDER)
            self.send(VERSION)
            self.send(id)
        except Exception as e:
            self.error(id, EClientErrors.FAIL_SEND_CORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqOpenOrders(self):
        """ generated source for method reqOpenOrders """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        #  send cancel order msg
        try:
            self.send(self.REQ_OPEN_ORDERS)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_OORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqIds(self, numIds):
        """ generated source for method reqIds """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        try:
            self.send(self.REQ_IDS)
            self.send(VERSION)
            self.send(numIds)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_CORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqNewsBulletins(self, allMsgs):
        """ generated source for method reqNewsBulletins """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        try:
            self.send(self.REQ_NEWS_BULLETINS)
            self.send(VERSION)
            self.send(allMsgs)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_CORDER, str(e))
            self.close()

    @synchronized(mlock)
    def cancelNewsBulletins(self):
        """ generated source for method cancelNewsBulletins """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        #  send cancel order msg
        try:
            self.send(self.CANCEL_NEWS_BULLETINS)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_CORDER, str(e))
            self.close()

    @synchronized(mlock)
    def setServerLogLevel(self, logLevel):
        """ generated source for method setServerLogLevel """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        #  send the set server logging level message
        try:
            self.send(self.SET_SERVER_LOGLEVEL)
            self.send(VERSION)
            self.send(logLevel)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_SERVER_LOG_LEVEL, str(e))
            self.close()

    @synchronized(mlock)
    def reqAutoOpenOrders(self, bAutoBind):
        """ generated source for method reqAutoOpenOrders """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        #  send req open orders msg
        try:
            self.send(self.REQ_AUTO_OPEN_ORDERS)
            self.send(VERSION)
            self.send(bAutoBind)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_OORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqAllOpenOrders(self):
        """ generated source for method reqAllOpenOrders """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        #  send req all open orders msg
        try:
            self.send(self.REQ_ALL_OPEN_ORDERS)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_OORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqManagedAccts(self):
        """ generated source for method reqManagedAccts """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        VERSION = 1
        #  send req FA managed accounts msg
        try:
            self.send(self.REQ_MANAGED_ACCTS)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_OORDER, str(e))
            self.close()

    @synchronized(mlock)
    def requestFA(self, faDataType):
        """ generated source for method requestFA """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        #  This feature is only available for versions of TWS >= 13
        if self.m_serverVersion < 13:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        VERSION = 1
        try:
            self.send(self.REQ_FA)
            self.send(VERSION)
            self.send(faDataType)
        except Exception as e:
            self.error(faDataType, EClientErrors.FAIL_SEND_FA_REQUEST, str(e))
            self.close()

    @synchronized(mlock)
    def replaceFA(self, faDataType, xml):
        """ generated source for method replaceFA """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        #  This feature is only available for versions of TWS >= 13
        if self.m_serverVersion < 13:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        VERSION = 1
        try:
            self.send(self.REPLACE_FA)
            self.send(VERSION)
            self.send(faDataType)
            self.send(xml)
        except Exception as e:
            self.error(faDataType, EClientErrors.FAIL_SEND_FA_REPLACE, str(e))
            self.close()

    @synchronized(mlock)
    def reqCurrentTime(self):
        """ generated source for method reqCurrentTime """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        #  This feature is only available for versions of TWS >= 33
        if self.m_serverVersion < 33:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support current time requests.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_CURRENT_TIME)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQCURRTIME, str(e))
            self.close()

    @synchronized(mlock)
    def reqFundamentalData(self, reqId, contract, reportType):
        """ generated source for method reqFundamentalData """
        # not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_FUNDAMENTAL_DATA:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support fundamental data requests.")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
            if contract.m_conId > 0:
                self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support conId parameter in reqFundamentalData.")
                return
        VERSION = 2
        try:
            #  send req fund data msg
            self.send(self.REQ_FUNDAMENTAL_DATA)
            self.send(VERSION)
            self.send(reqId)
            #  send contract fields
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_exchange)
            self.send(contract.m_primaryExch)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            self.send(reportType)
        except Exception as e:
            self.error(reqId, EClientErrors.FAIL_SEND_REQFUNDDATA, str(e))
            self.close()

    @synchronized(mlock)
    def cancelFundamentalData(self, reqId):
        """ generated source for method cancelFundamentalData """
        # not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_FUNDAMENTAL_DATA:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support fundamental data requests.")
            return
        VERSION = 1
        try:
            #  send req mkt data msg
            self.send(self.CANCEL_FUNDAMENTAL_DATA)
            self.send(VERSION)
            self.send(reqId)
        except Exception as e:
            self.error(reqId, EClientErrors.FAIL_SEND_CANFUNDDATA, str(e))
            self.close()

    @synchronized(mlock)
    def calculateImpliedVolatility(self, reqId, contract, optionPrice, underPrice):
        """ generated source for method calculateImpliedVolatility """
        # not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REQ_CALC_IMPLIED_VOLAT:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support calculate implied volatility requests.")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
            if not self.IsEmpty(contract.m_tradingClass):
                self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support tradingClass parameter in calculateImpliedVolatility.")
                return
        VERSION = 2
        try:
            #  send calculate implied volatility msg
            self.send(self.REQ_CALC_IMPLIED_VOLAT)
            self.send(VERSION)
            self.send(reqId)
            #  send contract fields
            self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            self.send(contract.m_primaryExch)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            self.send(optionPrice)
            self.send(underPrice)
        except Exception as e:
            self.error(reqId, EClientErrors.FAIL_SEND_REQCALCIMPLIEDVOLAT, str(e))
            self.close()

    @synchronized(mlock)
    def cancelCalculateImpliedVolatility(self, reqId):
        """ generated source for method cancelCalculateImpliedVolatility """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_CANCEL_CALC_IMPLIED_VOLAT:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support calculate implied volatility cancellation.")
            return
        VERSION = 1
        try:
            #  send cancel calculate implied volatility msg
            self.send(self.CANCEL_CALC_IMPLIED_VOLAT)
            self.send(VERSION)
            self.send(reqId)
        except Exception as e:
            self.error(reqId, EClientErrors.FAIL_SEND_CANCALCIMPLIEDVOLAT, str(e))
            self.close()

    @synchronized(mlock)
    def calculateOptionPrice(self, reqId, contract, volatility, underPrice):
        """ generated source for method calculateOptionPrice """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REQ_CALC_OPTION_PRICE:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support calculate option price requests.")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_TRADING_CLASS:
            if not self.IsEmpty(contract.m_tradingClass):
                self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support tradingClass parameter in calculateOptionPrice.")
                return
        VERSION = 2
        try:
            #  send calculate option price msg
            self.send(self.REQ_CALC_OPTION_PRICE)
            self.send(VERSION)
            self.send(reqId)
            #  send contract fields
            self.send(contract.m_conId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            self.send(contract.m_primaryExch)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            if self.m_serverVersion >= self.MIN_SERVER_VER_TRADING_CLASS:
                self.send(contract.m_tradingClass)
            self.send(volatility)
            self.send(underPrice)
        except Exception as e:
            self.error(reqId, EClientErrors.FAIL_SEND_REQCALCOPTIONPRICE, str(e))
            self.close()

    @synchronized(mlock)
    def cancelCalculateOptionPrice(self, reqId):
        """ generated source for method cancelCalculateOptionPrice """
        # not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_CANCEL_CALC_OPTION_PRICE:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support calculate option price cancellation.")
            return
        VERSION = 1
        try:
            #  send cancel calculate option price msg
            self.send(self.CANCEL_CALC_OPTION_PRICE)
            self.send(VERSION)
            self.send(reqId)
        except Exception as e:
            self.error(reqId, EClientErrors.FAIL_SEND_CANCALCOPTIONPRICE, str(e))
            self.close()

    @synchronized(mlock)
    def reqGlobalCancel(self):
        """ generated source for method reqGlobalCancel """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REQ_GLOBAL_CANCEL:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support globalCancel requests.")
            return
        VERSION = 1
        #  send request global cancel msg
        try:
            self.send(self.REQ_GLOBAL_CANCEL)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQGLOBALCANCEL, str(e))
            self.close()

    @synchronized(mlock)
    def reqMarketDataType(self, marketDataType):
        """ generated source for method reqMarketDataType """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REQ_MARKET_DATA_TYPE:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support marketDataType requests.")
            return
        VERSION = 1
        #  send the reqMarketDataType message
        try:
            self.send(self.REQ_MARKET_DATA_TYPE)
            self.send(VERSION)
            self.send(marketDataType)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQMARKETDATATYPE, str(e))
            self.close()

    @synchronized(mlock)
    def reqPositions(self):
        """ generated source for method reqPositions """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_ACCT_SUMMARY:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support position requests.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_POSITIONS)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQPOSITIONS, "" + e)

    @synchronized(mlock)
    def cancelPositions(self):
        """ generated source for method cancelPositions """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_ACCT_SUMMARY:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support position cancellation.")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_POSITIONS)
            self.send(VERSION)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_CANPOSITIONS, "" + e)

    @synchronized(mlock)
    def reqAccountSummary(self, reqId, group, tags):
        """ generated source for method reqAccountSummary """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_ACCT_SUMMARY:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support account summary requests.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_ACCOUNT_SUMMARY)
            self.send(VERSION)
            self.send(reqId)
            self.send(group)
            self.send(tags)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQACCOUNTDATA, "" + e)

    @synchronized(mlock)
    def cancelAccountSummary(self, reqId):
        """ generated source for method cancelAccountSummary """
        #  not connected?
        if not self.m_connected:
            self.notConnected()
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_ACCT_SUMMARY:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support account summary cancellation.")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_ACCOUNT_SUMMARY)
            self.send(VERSION)
            self.send(reqId)
        except Exception as e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_CANACCOUNTDATA, "" + e)

    #  @deprecated, never called. 
    @overloaded
    @synchronized(mlock)
    def error(self, err):
        """ generated source for method error """
        self.m_anyWrapper.error(err)

    @synchronized(mlock)
    @error.register(object, int, int, str)
    def error_0(self, id, errorCode, errorMsg):
        """ generated source for method error_0 """
        self.m_anyWrapper.error(id, errorCode, errorMsg)

    def close(self):
        """ generated source for method close """
        self.eDisconnect()
        self.wrapper().connectionClosed()

    @classmethod
    def is_(cls, strval):
        """ generated source for method is_ """
        #  return true if the string is not empty
        return strval is not None and len(strval) > 0

    @classmethod
    def isNull(cls, strval):
        """ generated source for method isNull """
        #  return true if the string is null or empty
        return not cls.is_(strval)

    @error.register(object, int, EClientErrors.CodeMsgPair, str)
    def error_1(self, id, pair, tail):
        """ generated source for method error_1 """
        self.error(id, pair.code(), pair.msg() + tail)

    @overloaded
    def send(self, strval):
        """ generated source for method send """
        #  write string to data buffer; writer thread will
        #  write it to socket
        if not self.IsEmpty(strval):
            self.m_dos.write(strval)
        self.sendEOL()

    def sendEOL(self):
        """ generated source for method sendEOL """
        self.m_dos.write(self.EOL)

    @send.register(object, int)
    def send_0(self, val):
        """ generated source for method send_0 """
        self.send(str(val))

    @send.register(object, str)
    def send_1(self, val):
        """ generated source for method send_1 """
        self.m_dos.write(val)
        self.sendEOL()

    @send.register(object, float)
    def send_2(self, val):
        """ generated source for method send_2 """
        self.send(str(val))

    @send.register(object, long)
    def send_3(self, val):
        """ generated source for method send_3 """
        self.send(str(val))

    @overloaded
    def sendMax(self, val):
        """ generated source for method sendMax """
        if val == Double.MAX_VALUE:
            self.sendEOL()
        else:
            self.send(str(val))

    @sendMax.register(object, int)
    def sendMax_0(self, val):
        """ generated source for method sendMax_0 """
        if val == Integer.MAX_VALUE:
            self.sendEOL()
        else:
            self.send(str(val))

    @send.register(object, bool)
    def send_4(self, val):
        """ generated source for method send_4 """
        self.send(1 if val else 0)

    @classmethod
    def IsEmpty(cls, strval):
        """ generated source for method IsEmpty """
        return Util.StringIsEmpty(strval)

    def notConnected(self):
        """ generated source for method notConnected """
        self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
