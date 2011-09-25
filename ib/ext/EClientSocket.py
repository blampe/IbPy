#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for EClientSocket.
##

# Source file: EClientSocket.java
# Target file: EClientSocket.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from logging import debug

from ib.ext.ComboLeg import ComboLeg
from ib.ext.EClientErrors import EClientErrors
from ib.ext.EReader import EReader
from ib.ext.Util import Util

from ib.lib.overloading import overloaded
from ib.lib import synchronized, Socket, DataInputStream, DataOutputStream
from ib.lib import Double, Integer

from threading import RLock
mlock = RLock()

class EClientSocket(object):
    """ generated source for EClientSocket

    """
    CLIENT_VERSION = 48
    SERVER_VERSION = 38
    EOL = 0
    BAG_SEC_TYPE = "BAG"
    GROUPS = 1
    PROFILES = 2
    ALIASES = 3

    @classmethod
    def faMsgTypeName(cls, faDataType):
        if faDataType == cls.GROUPS:
            return "GROUPS"
        elif faDataType == cls.PROFILES:
            return "PROFILES"
        elif faDataType == cls.ALIASES:
            return "ALIASES"
        return

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
    m_anyWrapper = None
    m_dos = None
    m_connected = bool()
    m_reader = None
    m_serverVersion = 0
    m_TwsTime = ""

    def serverVersion(self):
        return self.m_serverVersion

    def TwsConnectionTime(self):
        return self.m_TwsTime

    def wrapper(self):
        return self.m_anyWrapper

    def reader(self):
        return self.m_reader

    def __init__(self, anyWrapper):
        self.m_anyWrapper = anyWrapper

    def isConnected(self):
        return self.m_connected

    @overloaded
    @synchronized(mlock)
    def eConnect(self, host, port, clientId):
        host = self.checkConnected(host)
        if host is None:
            return
        try:
            socket = Socket(host, port)
            self.eConnect(socket, clientId)
        except (Exception, ):
            self.eDisconnect()
            self.connectionError()

    def connectionError(self):
        self.m_anyWrapper.error(EClientErrors.NO_VALID_ID, EClientErrors.CONNECT_FAIL.code(), EClientErrors.CONNECT_FAIL.msg())
        self.m_reader = None

    def checkConnected(self, host):
        if self.m_connected:
            self.m_anyWrapper.error(EClientErrors.NO_VALID_ID, EClientErrors.ALREADY_CONNECTED.code(), EClientErrors.ALREADY_CONNECTED.msg())
            return
        if self.isNull(host):
            host = "127.0.0.1"
        return host

    def createReader(self, socket, dis):
        return EReader(socket, dis)

    @eConnect.register(object, Socket, int)
    @synchronized(mlock)
    def eConnect_0(self, socket, clientId):
        self.m_dos = DataOutputStream(socket.getOutputStream())
        self.send(self.CLIENT_VERSION)
        self.m_reader = self.createReader(self, DataInputStream(socket.getInputStream()))
        self.m_serverVersion = self.m_reader.readInt()
        debug("Server Version:  %s", self.m_serverVersion)
        if self.m_serverVersion >= 20:
            self.m_TwsTime = self.m_reader.readStr()
            debug("TWS Time at connection:  %s", self.m_TwsTime)
        if self.m_serverVersion < self.SERVER_VERSION:
            self.eDisconnect()
            self.m_anyWrapper.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        if self.m_serverVersion >= 3:
            self.send(clientId)
        self.m_reader.start()
        self.m_connected = True

    @synchronized(mlock)
    def eDisconnect(self):
        if self.m_dos is None:
            return
        self.m_connected = False
        self.m_serverVersion = 0
        self.m_TwsTime = ""
        dos = self.m_dos
        self.m_dos = None
        self.reader = self.m_reader
        self.m_reader = None
        try:
            if self.reader is not None:
                self.reader.interrupt()
        except (Exception, ):
            pass
        try:
            if dos is not None:
                dos.close()
        except (Exception, ):
            pass

    @synchronized(mlock)
    def cancelScannerSubscription(self, tickerId):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 24:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support API scanner subscription.")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_SCANNER_SUBSCRIPTION)
            self.send(VERSION)
            self.send(tickerId)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANSCANNER, str(e))
            self.close()

    @synchronized(mlock)
    def reqScannerParameters(self):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 24:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support API scanner subscription.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_SCANNER_PARAMETERS)
            self.send(VERSION)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQSCANNERPARAMETERS, str(e))
            self.close()

    @synchronized(mlock)
    def reqScannerSubscription(self, tickerId, subscription):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
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
                self.send(subscription.averageOptionVolumeAbove())
                self.send(subscription.scannerSettingPairs())
            if self.m_serverVersion >= 27:
                self.send(subscription.stockTypeFilter())
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQSCANNER, str(e))
            self.close()

    @synchronized(mlock)
    def reqMktData(self, tickerId, contract, genericTickList, snapshot):
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
        VERSION = 9
        try:
            self.send(self.REQ_MKT_DATA)
            self.send(VERSION)
            self.send(tickerId)
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
            if self.m_serverVersion >= 8 and self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                if contract.m_comboLegs is None:
                    self.send(0)
                else:
                    self.send(len(contract.m_comboLegs))
                    comboLeg = ComboLeg()
                    ## for-while
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
                self.send(genericTickList)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SNAPSHOT_MKT_DATA:
                self.send(snapshot)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQMKT, str(e))
            self.close()

    @synchronized(mlock)
    def cancelHistoricalData(self, tickerId):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 24:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support historical data query cancellation.")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_HISTORICAL_DATA)
            self.send(VERSION)
            self.send(tickerId)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANHISTDATA, str(e))
            self.close()

    def cancelRealTimeBars(self, tickerId):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REAL_TIME_BARS:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support realtime bar data query cancellation.")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_REAL_TIME_BARS)
            self.send(VERSION)
            self.send(tickerId)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANRTBARS, str(e))
            self.close()

    @synchronized(mlock)
    def reqHistoricalData(self, tickerId,
                                contract,
                                endDateTime,
                                durationStr,
                                barSizeSetting,
                                whatToShow,
                                useRTH,
                                formatDate):
        if not self.m_connected:
            self.error(tickerId, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 4
        try:
            if self.m_serverVersion < 16:
                self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support historical data backfill.")
                return
            self.send(self.REQ_HISTORICAL_DATA)
            self.send(VERSION)
            self.send(tickerId)
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
                    comboLeg = ComboLeg()
                    ## for-while
                    i = 0
                    while i < len(contract.m_comboLegs):
                        comboLeg = contract.m_comboLegs[i]
                        self.send(comboLeg.m_conId)
                        self.send(comboLeg.m_ratio)
                        self.send(comboLeg.m_action)
                        self.send(comboLeg.m_exchange)
                        i += 1
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQHISTDATA, str(e))
            self.close()

    @synchronized(mlock)
    def reqRealTimeBars(self, tickerId,
                              contract,
                              barSize,
                              whatToShow,
                              useRTH):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REAL_TIME_BARS:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support real time bars.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_REAL_TIME_BARS)
            self.send(VERSION)
            self.send(tickerId)
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
            self.send(barSize)
            self.send(whatToShow)
            self.send(useRTH)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQRTBARS, str(e))
            self.close()

    @synchronized(mlock)
    def reqContractDetails(self, reqId, contract):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 4:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_SEC_ID_TYPE:
            if not self.IsEmpty(contract.m_secIdType) or not self.IsEmpty(contract.m_secId):
                self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support secIdType and secId parameters.")
                return
        VERSION = 6
        try:
            self.send(self.REQ_CONTRACT_DATA)
            self.send(VERSION)
            if self.m_serverVersion >= self.MIN_SERVER_VER_CONTRACT_DATA_CHAIN:
                self.send(reqId)
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
            if self.m_serverVersion >= 31:
                self.send(contract.m_includeExpired)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SEC_ID_TYPE:
                self.send(contract.m_secIdType)
                self.send(contract.m_secId)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQCONTRACT, str(e))
            self.close()

    @synchronized(mlock)
    def reqMktDepth(self, tickerId, contract, numRows):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 6:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        VERSION = 3
        try:
            self.send(self.REQ_MKT_DEPTH)
            self.send(VERSION)
            self.send(tickerId)
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
            if self.m_serverVersion >= 19:
                self.send(numRows)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQMKTDEPTH, str(e))
            self.close()

    @synchronized(mlock)
    def cancelMktData(self, tickerId):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_MKT_DATA)
            self.send(VERSION)
            self.send(tickerId)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANMKT, str(e))
            self.close()

    @synchronized(mlock)
    def cancelMktDepth(self, tickerId):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 6:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_MKT_DEPTH)
            self.send(VERSION)
            self.send(tickerId)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_CANMKTDEPTH, str(e))
            self.close()

    @synchronized(mlock)
    def exerciseOptions(self, tickerId,
                              contract,
                              exerciseAction,
                              exerciseQuantity,
                              account,
                              override):
        if not self.m_connected:
            self.error(tickerId, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            if self.m_serverVersion < 21:
                self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support options exercise from the API.")
                return
            self.send(self.EXERCISE_OPTIONS)
            self.send(VERSION)
            self.send(tickerId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_expiry)
            self.send(contract.m_strike)
            self.send(contract.m_right)
            self.send(contract.m_multiplier)
            self.send(contract.m_exchange)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            self.send(exerciseAction)
            self.send(exerciseQuantity)
            self.send(account)
            self.send(override)
        except (Exception, ), e:
            self.error(tickerId, EClientErrors.FAIL_SEND_REQMKT, str(e))
            self.close()

    @synchronized(mlock)
    def placeOrder(self, id, contract, order):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_SCALE_ORDERS:
            if (order.m_scaleInitLevelSize != Integer.MAX_VALUE) or (order.m_scalePriceIncrement != Double.MAX_VALUE):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support Scale orders.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SSHORT_COMBO_LEGS:
            if not contract.m_comboLegs.isEmpty():
                comboLeg = ComboLeg()
                ## for-while
                i = 0
                while i < len(contract.m_comboLegs):
                    comboLeg = contract.m_comboLegs[i]
                    if (comboLeg.m_shortSaleSlot != 0) or not self.IsEmpty(comboLeg.m_designatedLocation):
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
            if (order.m_scaleSubsLevelSize != Integer.MAX_VALUE):
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
            if (order.m_exemptCode != -1):
                self.error(id, EClientErrors.UPDATE_TWS, "  It does not support exemptCode parameter.")
                return
        if self.m_serverVersion < self.MIN_SERVER_VER_SSHORTX:
            if not contract.m_comboLegs.isEmpty():
                comboLeg = ComboLeg()
                ## for-while
                i = 0
                while i < len(contract.m_comboLegs):
                    comboLeg = contract.m_comboLegs[i]
                    if (comboLeg.m_exemptCode != -1):
                        self.error(id, EClientErrors.UPDATE_TWS, "  It does not support exemptCode parameter.")
                        return
                    i += 1
        VERSION = 27 if self.m_serverVersion < self.MIN_SERVER_VER_NOT_HELD else 31
        try:
            self.send(self.PLACE_ORDER)
            self.send(VERSION)
            self.send(id)
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
            if self.m_serverVersion >= self.MIN_SERVER_VER_SEC_ID_TYPE:
                self.send(contract.m_secIdType)
                self.send(contract.m_secId)
            self.send(order.m_action)
            self.send(order.m_totalQuantity)
            self.send(order.m_orderType)
            self.send(order.m_lmtPrice)
            self.send(order.m_auxPrice)
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
                    self.send(False)
                else:
                    self.send(order.m_outsideRth)
            if self.m_serverVersion >= 7:
                self.send(order.m_hidden)
            if self.m_serverVersion >= 8 and self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                if contract.m_comboLegs is None:
                    self.send(0)
                else:
                    self.send(len(contract.m_comboLegs))
                    comboLeg = ComboLeg()
                    ## for-while
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
            if self.m_serverVersion >= 9:
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
                self.send(order.m_shortSaleSlot)
                self.send(order.m_designatedLocation)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SSHORTX_OLD:
                self.send(order.m_exemptCode)
            if self.m_serverVersion >= 19:
                self.send(order.m_ocaType)
                if self.m_serverVersion < 38:
                    self.send(False)
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
                lower = Double.MAX_VALUE if (self.m_serverVersion == 26) and order.m_orderType == "VOL" else order.m_stockRangeLower
                upper = Double.MAX_VALUE if (self.m_serverVersion == 26) and order.m_orderType == "VOL" else order.m_stockRangeUpper
                self.sendMax(lower)
                self.sendMax(upper)
            if self.m_serverVersion >= 22:
                self.send(order.m_overridePercentageConstraints)
            if self.m_serverVersion >= 26:
                self.sendMax(order.m_volatility)
                self.sendMax(order.m_volatilityType)
                if self.m_serverVersion < 28:
                    self.send(order.m_deltaNeutralOrderType.lower() == "MKT".lower())
                else:
                    self.send(order.m_deltaNeutralOrderType)
                    self.sendMax(order.m_deltaNeutralAuxPrice)
                self.send(order.m_continuousUpdate)
                if (self.m_serverVersion == 26):
                    lower = order.m_stockRangeLower if order.m_orderType == "VOL" else Double.MAX_VALUE
                    upper = order.m_stockRangeUpper if order.m_orderType == "VOL" else Double.MAX_VALUE
                    self.sendMax(lower)
                    self.sendMax(upper)
                self.sendMax(order.m_referencePriceType)
            if self.m_serverVersion >= 30:
                self.sendMax(order.m_trailStopPrice)
            if self.m_serverVersion >= self.MIN_SERVER_VER_SCALE_ORDERS:
                if self.m_serverVersion >= self.MIN_SERVER_VER_SCALE_ORDERS2:
                    self.sendMax(order.m_scaleInitLevelSize)
                    self.sendMax(order.m_scaleSubsLevelSize)
                else:
                    self.send("")
                    self.sendMax(order.m_scaleInitLevelSize)
                self.sendMax(order.m_scalePriceIncrement)
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
                        ## for-while
                        i = 0
                        while i < algoParamsCount:
                            tagValue = algoParams[i]
                            self.send(tagValue.m_tag)
                            self.send(tagValue.m_value)
                            i += 1
            if self.m_serverVersion >= self.MIN_SERVER_VER_WHAT_IF_ORDERS:
                self.send(order.m_whatIf)
        except (Exception, ), e:
            self.error(id, EClientErrors.FAIL_SEND_ORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqAccountUpdates(self, subscribe, acctCode):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 2
        try:
            self.send(self.REQ_ACCOUNT_DATA)
            self.send(VERSION)
            self.send(subscribe)
            if self.m_serverVersion >= 9:
                self.send(acctCode)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_ACCT, str(e))
            self.close()

    @synchronized(mlock)
    def reqExecutions(self, reqId, filter):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 3
        try:
            self.send(self.REQ_EXECUTIONS)
            self.send(VERSION)
            if self.m_serverVersion >= self.MIN_SERVER_VER_EXECUTION_DATA_CHAIN:
                self.send(reqId)
            if self.m_serverVersion >= 9:
                self.send(filter.m_clientId)
                self.send(filter.m_acctCode)
                self.send(filter.m_time)
                self.send(filter.m_symbol)
                self.send(filter.m_secType)
                self.send(filter.m_exchange)
                self.send(filter.m_side)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_EXEC, str(e))
            self.close()

    @synchronized(mlock)
    def cancelOrder(self, id):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_ORDER)
            self.send(VERSION)
            self.send(id)
        except (Exception, ), e:
            self.error(id, EClientErrors.FAIL_SEND_CORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqOpenOrders(self):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.REQ_OPEN_ORDERS)
            self.send(VERSION)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_OORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqIds(self, numIds):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.REQ_IDS)
            self.send(VERSION)
            self.send(numIds)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_CORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqNewsBulletins(self, allMsgs):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.REQ_NEWS_BULLETINS)
            self.send(VERSION)
            self.send(allMsgs)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_CORDER, str(e))
            self.close()

    @synchronized(mlock)
    def cancelNewsBulletins(self):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_NEWS_BULLETINS)
            self.send(VERSION)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_CORDER, str(e))
            self.close()

    @synchronized(mlock)
    def setServerLogLevel(self, logLevel):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.SET_SERVER_LOGLEVEL)
            self.send(VERSION)
            self.send(logLevel)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_SERVER_LOG_LEVEL, str(e))
            self.close()

    @synchronized(mlock)
    def reqAutoOpenOrders(self, bAutoBind):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.REQ_AUTO_OPEN_ORDERS)
            self.send(VERSION)
            self.send(bAutoBind)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_OORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqAllOpenOrders(self):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.REQ_ALL_OPEN_ORDERS)
            self.send(VERSION)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_OORDER, str(e))
            self.close()

    @synchronized(mlock)
    def reqManagedAccts(self):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        VERSION = 1
        try:
            self.send(self.REQ_MANAGED_ACCTS)
            self.send(VERSION)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_OORDER, str(e))
            self.close()

    @synchronized(mlock)
    def requestFA(self, faDataType):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 13:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        VERSION = 1
        try:
            self.send(self.REQ_FA)
            self.send(VERSION)
            self.send(faDataType)
        except (Exception, ), e:
            self.error(faDataType, EClientErrors.FAIL_SEND_FA_REQUEST, str(e))
            self.close()

    @synchronized(mlock)
    def replaceFA(self, faDataType, xml):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 13:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code(), EClientErrors.UPDATE_TWS.msg())
            return
        VERSION = 1
        try:
            self.send(self.REPLACE_FA)
            self.send(VERSION)
            self.send(faDataType)
            self.send(xml)
        except (Exception, ), e:
            self.error(faDataType, EClientErrors.FAIL_SEND_FA_REPLACE, str(e))
            self.close()

    @synchronized(mlock)
    def reqCurrentTime(self):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < 33:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support current time requests.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_CURRENT_TIME)
            self.send(VERSION)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQCURRTIME, str(e))
            self.close()

    @synchronized(mlock)
    def reqFundamentalData(self, reqId, contract, reportType):
        if not self.m_connected:
            self.error(reqId, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_FUNDAMENTAL_DATA:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support fundamental data requests.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_FUNDAMENTAL_DATA)
            self.send(VERSION)
            self.send(reqId)
            self.send(contract.m_symbol)
            self.send(contract.m_secType)
            self.send(contract.m_exchange)
            self.send(contract.m_primaryExch)
            self.send(contract.m_currency)
            self.send(contract.m_localSymbol)
            self.send(reportType)
        except (Exception, ), e:
            self.error(reqId, EClientErrors.FAIL_SEND_REQFUNDDATA, str(e))
            self.close()

    @synchronized(mlock)
    def cancelFundamentalData(self, reqId):
        if not self.m_connected:
            self.error(reqId, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_FUNDAMENTAL_DATA:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support fundamental data requests.")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_FUNDAMENTAL_DATA)
            self.send(VERSION)
            self.send(reqId)
        except (Exception, ), e:
            self.error(reqId, EClientErrors.FAIL_SEND_CANFUNDDATA, str(e))
            self.close()

    @synchronized(mlock)
    def calculateImpliedVolatility(self, reqId, contract, optionPrice, underPrice):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REQ_CALC_IMPLIED_VOLAT:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support calculate implied volatility requests.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_CALC_IMPLIED_VOLAT)
            self.send(VERSION)
            self.send(reqId)
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
            self.send(optionPrice)
            self.send(underPrice)
        except (Exception, ), e:
            self.error(reqId, EClientErrors.FAIL_SEND_REQCALCIMPLIEDVOLAT, str(e))
            self.close()

    @synchronized(mlock)
    def cancelCalculateImpliedVolatility(self, reqId):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_CANCEL_CALC_IMPLIED_VOLAT:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support calculate implied volatility cancellation.")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_CALC_IMPLIED_VOLAT)
            self.send(VERSION)
            self.send(reqId)
        except (Exception, ), e:
            self.error(reqId, EClientErrors.FAIL_SEND_CANCALCIMPLIEDVOLAT, str(e))
            self.close()

    @synchronized(mlock)
    def calculateOptionPrice(self, reqId, contract, volatility, underPrice):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REQ_CALC_OPTION_PRICE:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support calculate option price requests.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_CALC_OPTION_PRICE)
            self.send(VERSION)
            self.send(reqId)
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
            self.send(volatility)
            self.send(underPrice)
        except (Exception, ), e:
            self.error(reqId, EClientErrors.FAIL_SEND_REQCALCOPTIONPRICE, str(e))
            self.close()

    @synchronized(mlock)
    def cancelCalculateOptionPrice(self, reqId):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_CANCEL_CALC_OPTION_PRICE:
            self.error(reqId, EClientErrors.UPDATE_TWS, "  It does not support calculate option price cancellation.")
            return
        VERSION = 1
        try:
            self.send(self.CANCEL_CALC_OPTION_PRICE)
            self.send(VERSION)
            self.send(reqId)
        except (Exception, ), e:
            self.error(reqId, EClientErrors.FAIL_SEND_CANCALCOPTIONPRICE, str(e))
            self.close()

    @synchronized(mlock)
    def reqGlobalCancel(self):
        if not self.m_connected:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED, "")
            return
        if self.m_serverVersion < self.MIN_SERVER_VER_REQ_GLOBAL_CANCEL:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS, "  It does not support globalCancel requests.")
            return
        VERSION = 1
        try:
            self.send(self.REQ_GLOBAL_CANCEL)
            self.send(VERSION)
        except (Exception, ), e:
            self.error(EClientErrors.NO_VALID_ID, EClientErrors.FAIL_SEND_REQGLOBALCANCEL, str(e))
            self.close()

    @overloaded
    @synchronized(mlock)
    def error(self, err):
        self.m_anyWrapper.error(err)

    @error.register(object, int, int, str)
    @synchronized(mlock)
    def error_0(self, id, errorCode, errorMsg):
        self.m_anyWrapper.error(id, errorCode, errorMsg)

    def close(self):
        self.eDisconnect()
        self.wrapper().connectionClosed()

    @classmethod
    def is_(cls, strval):
        return strval is not None and len(strval) > 0

    @classmethod
    def isNull(cls, strval):
        return not cls.is_(strval)

    @error.register(object, int, EClientErrors.CodeMsgPair, str)
    def error_1(self, id, pair, tail):
        self.error(id, pair.code(), pair.msg() + tail)

    @overloaded
    def send(self, strval):
        if not self.IsEmpty(strval):
            self.m_dos.write(strval.getBytes())
        self.sendEOL()

    def sendEOL(self):
        self.m_dos.write(self.EOL)

    @send.register(object, int)
    def send_0(self, val):
        self.send(str(val))

    @send.register(object, str)
    def send_1(self, val):
        self.m_dos.write(val)
        self.sendEOL()

    @send.register(object, float)
    def send_2(self, val):
        self.send(str(val))

    @send.register(object, long)
    def send_3(self, val):
        self.send(str(val))

    @overloaded
    def sendMax(self, val):
        if (val == Double.MAX_VALUE):
            self.sendEOL()
        else:
            self.send(str(val))

    @sendMax.register(object, int)
    def sendMax_0(self, val):
        if (val == Integer.MAX_VALUE):
            self.sendEOL()
        else:
            self.send(str(val))

    @send.register(object, bool)
    def send_4(self, val):
        self.send(1 if val else 0)

    @classmethod
    def IsEmpty(cls, strval):
        return Util.StringIsEmpty(strval)


