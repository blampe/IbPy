#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

    @overloaded
    def __init__(self):
        self.m_conId = 0
        self.m_ratio = 0
        self.m_openClose = 0

    @__init__.register(object, int, int, str, str, int)
    def __init___0(self, p_ConId, 
                         p_Ratio, 
                         p_Action, 
                         p_exchange, 
                         p_openClose):
        self.m_conId = p_ConId
        self.m_ratio = p_Ratio
        self.m_action = p_Action
        self.m_exchange = p_exchange
        self.m_openClose = p_openClose

    def __eq__(self, p_other):
        if self is p_other:
            return True
        else:
            if p_other is None:
                return False
        l_theOther = p_other
        l_thisAction = self.m_action if self.m_action != None else "" 
        l_thisExchange = self.m_exchange if self.m_exchange != None else "" 
        return l_thisAction.compareToIgnoreCase(l_theOther.m_action) == 0 and l_thisExchange.compareToIgnoreCase(l_theOther.m_exchange) == 0 and self.m_conId == l_theOther.m_conId and self.m_ratio == l_theOther.m_ratio and self.m_openClose == l_theOther.m_openClose


