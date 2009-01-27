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
    def StringIsEmpty(cls, strval):
        return strval is None or (len(strval) == 0)

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
    def VectorEqualsUnordered(cls, lhs, rhs):
        if (lhs == rhs):
            return True
        lhsCount = 0 if lhs is None else len(lhs)
        rhsCount = 0 if rhs is None else len(rhs)
        if (lhsCount != rhsCount):
            return False
        if (lhsCount == 0):
            return True
        matchedRhsElems = [bool() for __idx0 in range(rhsCount)]
        ## for-while
        lhsIdx = 0
        while lhsIdx < lhsCount:
            lhsElem = lhs[lhsIdx]
            rhsIdx = 0
            ## for-while
            while rhsIdx < rhsCount:
                if matchedRhsElems[rhsIdx]:
                    continue
                if lhsElem == rhs[rhsIdx]:
                    matchedRhsElems[rhsIdx] = True
                    break
                rhsIdx += 1
            if rhsIdx >= rhsCount:
                return False
            lhsIdx += 1
        return True

    @classmethod
    def IntMaxString(cls, value):
        return "" if (value == Integer.MAX_VALUE) else str(value)

    @classmethod
    def DoubleMaxString(cls, value):
        return "" if (value == Double.MAX_VALUE) else str(value)


