#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translation source for ContractDetails.
##

# Source file: ContractDetails.java
# Target file: ContractDetails.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.

from ib.lib.overloading import overloaded
from ib.ext.Contract import Contract

class ContractDetails(object):
    """ generated source for ContractDetails

    """
    m_summary = None
    m_marketName = ""
    m_tradingClass = ""
    m_conid = 0
    m_minTick = float()
    m_multiplier = ""
    m_priceMagnifier = 0
    m_orderTypes = ""
    m_validExchanges = ""

    @overloaded
    def __init__(self):
        self.m_summary = Contract()
        self.m_conid = 0
        self.m_minTick = 0

    @__init__.register(object, Contract, str, str, int, float, str, str, str)
    def __init___0(self, p_summary,
                         p_marketName,
                         p_tradingClass,
                         p_conid,
                         p_minTick,
                         p_multiplier,
                         p_orderTypes,
                         p_validExchanges):
        self.m_summary = p_summary
        self.m_marketName = p_marketName
        self.m_tradingClass = p_tradingClass
        self.m_conid = p_conid
        self.m_minTick = p_minTick
        self.m_multiplier = p_multiplier
        self.m_orderTypes = p_orderTypes
        self.m_validExchanges = p_validExchanges


