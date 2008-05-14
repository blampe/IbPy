#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for ExecutionFilter.
##

# Source file: ExecutionFilter.java
# Target file: ExecutionFilter.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib.overloading import overloaded

class ExecutionFilter(object):
    """ generated source for ExecutionFilter

    """
    m_clientId = 0
    m_acctCode = ""
    m_time = ""
    m_symbol = ""
    m_secType = ""
    m_exchange = ""
    m_side = ""

    @overloaded
    def __init__(self):
        self.m_clientId = 0

    @__init__.register(object, int, str, str, str, str, str, str)
    def __init___0(self, p_clientId,
                         p_acctCode,
                         p_time,
                         p_symbol,
                         p_secType,
                         p_exchange,
                         p_side):
        self.m_clientId = p_clientId
        self.m_acctCode = p_acctCode
        self.m_time = p_time
        self.m_symbol = p_symbol
        self.m_secType = p_secType
        self.m_exchange = p_exchange
        self.m_side = p_side

    def __eq__(self, p_other):
        l_bRetVal = False
        if p_other is None:
            l_bRetVal = False
        else:
            if self is p_other:
                l_bRetVal = True
            else:
                l_theOther = p_other
                l_bRetVal = (self.m_clientId == l_theOther.m_clientId) and self.m_acctCode.lower() == l_theOther.m_acctCode.lower() and self.m_time.lower() == l_theOther.m_time.lower() and self.m_symbol.lower() == l_theOther.m_symbol.lower() and self.m_secType.lower() == l_theOther.m_secType.lower() and self.m_exchange.lower() == l_theOther.m_exchange.lower() and self.m_side.lower() == l_theOther.m_side.lower()
        return l_bRetVal


