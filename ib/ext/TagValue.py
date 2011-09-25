#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for TagValue.
##

# Source file: TagValue.java
# Target file: TagValue.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib.overloading import overloaded
from ib.ext.Util import Util

class TagValue(object):
    """ generated source for TagValue

    """
    m_tag = ""
    m_value = ""

    @overloaded
    def __init__(self):
        pass

    @__init__.register(object, str, str)
    def __init___0(self, p_tag, p_value):
        self.m_tag = p_tag
        self.m_value = p_value

    def __eq__(self, p_other):
        if self is p_other:
            return True
        if p_other is None:
            return False
        l_theOther = p_other
        if (Util.StringCompare(self.m_tag, l_theOther.m_tag) != 0) or (Util.StringCompare(self.m_value, l_theOther.m_value) != 0):
            return False
        return True


