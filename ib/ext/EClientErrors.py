#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for EClientErrors.
##

# Source file: EClientErrors.java
# Target file: EClientErrors.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.


class EClientErrors(object):
    """ generated source for EClientErrors

    """
    class CodeMsgPair(object):
        """ generated source for CodeMsgPair

        """
        m_errorCode = 0
        m_errorMsg = ""

        def code(self):
            return self.m_errorCode

        def msg(self):
            return self.m_errorMsg

        def __init__(self, i, errString):
            self.m_errorCode = i
            self.m_errorMsg = errString

    NO_VALID_ID = -1
    ALREADY_CONNECTED = CodeMsgPair(501, "Already connected.")
    CONNECT_FAIL = CodeMsgPair(502, "Couldn't connect to TWS.  Confirm that \"Enable ActiveX and Socket Clients\" is enabled on the TWS \"Configure->API\" menu.")
    UPDATE_TWS = CodeMsgPair(503, "The TWS is out of date and must be upgraded.")
    NOT_CONNECTED = CodeMsgPair(504, "Not connected")
    UNKNOWN_ID = CodeMsgPair(505, "Fatal Error: Unknown message id.")
    FAIL_SEND_REQMKT = CodeMsgPair(510, "Request Market Data Sending Error - ")
    FAIL_SEND_CANMKT = CodeMsgPair(511, "Cancel Market Data Sending Error - ")
    FAIL_SEND_ORDER = CodeMsgPair(512, "Order Sending Error - ")
    FAIL_SEND_ACCT = CodeMsgPair(513, "Account Update Request Sending Error -")
    FAIL_SEND_EXEC = CodeMsgPair(514, "Request For Executions Sending Error -")
    FAIL_SEND_CORDER = CodeMsgPair(515, "Cancel Order Sending Error -")
    FAIL_SEND_OORDER = CodeMsgPair(516, "Request Open Order Sending Error -")
    UNKNOWN_CONTRACT = CodeMsgPair(517, "Unknown contract. Verify the contract details supplied.")
    FAIL_SEND_REQCONTRACT = CodeMsgPair(518, "Request Contract Data Sending Error - ")
    FAIL_SEND_REQMKTDEPTH = CodeMsgPair(519, "Request Market Depth Sending Error - ")
    FAIL_SEND_CANMKTDEPTH = CodeMsgPair(520, "Cancel Market Depth Sending Error - ")
    FAIL_SEND_SERVER_LOG_LEVEL = CodeMsgPair(521, "Set Server Log Level Sending Error - ")
    FAIL_SEND_FA_REQUEST = CodeMsgPair(522, "FA Information Request Sending Error - ")
    FAIL_SEND_FA_REPLACE = CodeMsgPair(523, "FA Information Replace Sending Error - ")
    FAIL_SEND_REQSCANNER = CodeMsgPair(524, "Request Scanner Subscription Sending Error - ")
    FAIL_SEND_CANSCANNER = CodeMsgPair(525, "Cancel Scanner Subscription Sending Error - ")
    FAIL_SEND_REQSCANNERPARAMETERS = CodeMsgPair(526, "Request Scanner Parameter Sending Error - ")
    FAIL_SEND_REQHISTDATA = CodeMsgPair(527, "Request Historical Data Sending Error - ")
    FAIL_SEND_CANHISTDATA = CodeMsgPair(528, "Request Historical Data Sending Error - ")
    FAIL_SEND_REQRTBARS = CodeMsgPair(529, "Request Real-time Bar Data Sending Error - ")
    FAIL_SEND_CANRTBARS = CodeMsgPair(530, "Cancel Real-time Bar Data Sending Error - ")
    FAIL_SEND_REQCURRTIME = CodeMsgPair(531, "Request Current Time Sending Error - ")
    FAIL_SEND_REQFUNDDATA = CodeMsgPair(532, "Request Fundamental Data Sending Error - ")
    FAIL_SEND_CANFUNDDATA = CodeMsgPair(533, "Cancel Fundamental Data Sending Error - ")
    FAIL_SEND_REQCALCIMPLIEDVOLAT = CodeMsgPair(534, "Request Calculate Implied Volatility Sending Error - ")
    FAIL_SEND_REQCALCOPTIONPRICE = CodeMsgPair(535, "Request Calculate Option Price Sending Error - ")
    FAIL_SEND_CANCALCIMPLIEDVOLAT = CodeMsgPair(536, "Cancel Calculate Implied Volatility Sending Error - ")
    FAIL_SEND_CANCALCOPTIONPRICE = CodeMsgPair(537, "Cancel Calculate Option Price Sending Error - ")
    FAIL_SEND_REQGLOBALCANCEL = CodeMsgPair(538, "Request Global Cancel Sending Error - ")

    def __init__(self):
        pass


