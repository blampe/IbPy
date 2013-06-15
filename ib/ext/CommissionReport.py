#!/usr/bin/env python
""" generated source for module CommissionReport """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

# 
#  * CommissionReport.java
#  *
#  
# package: com.ib.client
class CommissionReport(object):
    """ generated source for class CommissionReport """
    m_execId = ""
    m_commission = float()
    m_currency = ""
    m_realizedPNL = float()
    m_yield = float()
    m_yieldRedemptionDate = 0   #  YYYYMMDD format

    def __init__(self):
        """ generated source for method __init__ """
        self.m_commission = 0
        self.m_realizedPNL = 0
        self.m_yield = 0
        self.m_yieldRedemptionDate = 0

    def __eq__(self, p_other):
        """ generated source for method equals """
        l_bRetVal = False
        if p_other is None:
            l_bRetVal = False
        elif self is p_other:
            l_bRetVal = True
        else:
            l_bRetVal = self.m_execId == p_other.m_execId
        return l_bRetVal

