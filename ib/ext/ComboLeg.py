#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for ComboLeg.
##

# Source file: ComboLeg.java
# Target file: ComboLeg.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib.overloading import overloaded
from ib.ext.Util import Util

class ComboLeg(object):
    """ generated source for ComboLeg

    """
    SAME = 0
    OPEN = 1
    CLOSE = 2
    UNKNOWN = 3
    m_conId = 0
    m_ratio = 0
    m_action = ""
    m_exchange = ""
    m_openClose = 0
    m_shortSaleSlot = 0
    m_designatedLocation = ""
    m_exemptCode = 0

    @overloaded
    def __init__(self):
        pass # super(ComboLeg, self).__init__(0, 0, None, None, 0, 0, None, -1)

    @__init__.register(object, int, int, str, str, int)
    def __init___0(self, p_conId,
                         p_ratio,
                         p_action,
                         p_exchange,
                         p_openClose):
        pass # super(ComboLeg, self).__init__(p_conId, p_ratio, p_action, p_exchange, p_openClose, 0, None, -1)

    @__init__.register(object, int, int, str, str, int, int, str)
    def __init___1(self, p_conId,
                         p_ratio,
                         p_action,
                         p_exchange,
                         p_openClose,
                         p_shortSaleSlot,
                         p_designatedLocation):
        pass # super(ComboLeg, self).__init__(p_conId, p_ratio, p_action, p_exchange, p_openClose, p_shortSaleSlot, p_designatedLocation, -1)

    @__init__.register(object, int, int, str, str, int, int, str, int)
    def __init___2(self, p_conId,
                         p_ratio,
                         p_action,
                         p_exchange,
                         p_openClose,
                         p_shortSaleSlot,
                         p_designatedLocation,
                         p_exemptCode):
        self.m_conId = p_conId
        self.m_ratio = p_ratio
        self.m_action = p_action
        self.m_exchange = p_exchange
        self.m_openClose = p_openClose
        self.m_shortSaleSlot = p_shortSaleSlot
        self.m_designatedLocation = p_designatedLocation
        self.m_exemptCode = p_exemptCode

    def __eq__(self, p_other):
        if self is p_other:
            return True
        else:
            if p_other is None:
                return False
        l_theOther = p_other
        if (self.m_conId != l_theOther.m_conId) or (self.m_ratio != l_theOther.m_ratio) or (self.m_openClose != l_theOther.m_openClose) or (self.m_shortSaleSlot != l_theOther.m_shortSaleSlot) or (self.m_exemptCode != l_theOther.m_exemptCode):
            return False
        if (Util.StringCompareIgnCase(self.m_action, l_theOther.m_action) != 0) or (Util.StringCompareIgnCase(self.m_exchange, l_theOther.m_exchange) != 0) or (Util.StringCompareIgnCase(self.m_designatedLocation, l_theOther.m_designatedLocation) != 0):
            return False
        return True


