#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for Util.
##

# Source file: Util.java
# Target file: Util.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib import Double, Integer

class Util(object):
    """ generated source for Util

    """

    @classmethod
    def NormalizeString(cls, strval):
        return strval if strval is not None else ""

    @classmethod
    def StringCompare(cls, lhs, rhs):
        return cmp(str(lhs), str(rhs))

    @classmethod
    def StringCompareIgnCase(cls, lhs, rhs):
        return cmp(str(lhs).lower(), str(rhs).lower())

    @classmethod
    def IntMaxString(cls, value):
        return "" if (value == Integer.MAX_VALUE) else str(value)

    @classmethod
    def DoubleMaxString(cls, value):
        return "" if (value == Double.MAX_VALUE) else str(value)


