#!/usr/bin/env python
""" generated source for module OrderState """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib.overloading import overloaded
from ib.ext.Util import Util
# 
#  * OrderState.java
#  
# package: com.ib.client
class OrderState(object):
    """ generated source for class OrderState """
    m_status = ""
    m_initMargin = ""
    m_maintMargin = ""
    m_equityWithLoan = ""
    m_commission = float()
    m_minCommission = float()
    m_maxCommission = float()
    m_commissionCurrency = ""
    m_warningText = ""

    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        pass # super(OrderState, self).__init__(None, None, None, None, 0.0, 0.0, 0.0, None, None)

    @__init__.register(object, str, str, str, str, float, float, float, str, str)
    def __init___0(self, status, initMargin, maintMargin, equityWithLoan, commission, minCommission, maxCommission, commissionCurrency, warningText):
        """ generated source for method __init___0 """
        self.m_initMargin = initMargin
        self.m_maintMargin = maintMargin
        self.m_equityWithLoan = equityWithLoan
        self.m_commission = commission
        self.m_minCommission = minCommission
        self.m_maxCommission = maxCommission
        self.m_commissionCurrency = commissionCurrency
        self.m_warningText = warningText

    def __eq__(self, other):
        """ generated source for method equals """
        if self == other:
            return True
        if other is None:
            return False
        state = other
        if self.m_commission != state.m_commission or self.m_minCommission != state.m_minCommission or self.m_maxCommission != state.m_maxCommission:
            return False
        if Util.StringCompare(self.m_status, state.m_status) != 0 or Util.StringCompare(self.m_initMargin, state.m_initMargin) != 0 or Util.StringCompare(self.m_maintMargin, state.m_maintMargin) != 0 or Util.StringCompare(self.m_equityWithLoan, state.m_equityWithLoan) != 0 or Util.StringCompare(self.m_commissionCurrency, state.m_commissionCurrency) != 0:
            return False
        return True

