#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for Execution.
##

# Source file: Execution.java
# Target file: Execution.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib.overloading import overloaded

class Execution(object):
    """ generated source for Execution

    """
    m_orderId = 0
    m_clientId = 0
    m_execId = ""
    m_time = ""
    m_acctNumber = ""
    m_exchange = ""
    m_side = ""
    m_shares = 0
    m_price = float()
    m_permId = 0
    m_liquidation = 0
    m_cumQty = 0
    m_avgPrice = float()

    @overloaded
    def __init__(self):
        self.m_orderId = 0
        self.m_clientId = 0
        self.m_shares = 0
        self.m_price = 0
        self.m_permId = 0
        self.m_liquidation = 0
        self.m_cumQty = 0
        self.m_avgPrice = 0

    @__init__.register(object, int, int, str, str, str, str, str, int, float, int, int, int, float)
    def __init___0(self, p_orderId,
                         p_clientId,
                         p_execId,
                         p_time,
                         p_acctNumber,
                         p_exchange,
                         p_side,
                         p_shares,
                         p_price,
                         p_permId,
                         p_liquidation,
                         p_cumQty,
                         p_avgPrice):
        self.m_orderId = p_orderId
        self.m_clientId = p_clientId
        self.m_execId = p_execId
        self.m_time = p_time
        self.m_acctNumber = p_acctNumber
        self.m_exchange = p_exchange
        self.m_side = p_side
        self.m_shares = p_shares
        self.m_price = p_price
        self.m_permId = p_permId
        self.m_liquidation = p_liquidation
        self.m_cumQty = p_cumQty
        self.m_avgPrice = p_avgPrice

    def __eq__(self, p_other):
        l_bRetVal = False
        if p_other is None:
            l_bRetVal = False
        else:
            if self is p_other:
                l_bRetVal = True
            else:
                l_theOther = p_other
                l_bRetVal = self.m_execId == l_theOther.m_execId
        return l_bRetVal


