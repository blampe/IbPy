#!/usr/bin/env python
""" generated source for module Util """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib import Double, Integer
# 
#  * Util.java
#  
# package: com.ib.client


class Util(object):
    """ generated source for class Util """
    @classmethod
    def StringIsEmpty(cls, strval):
        """ generated source for method StringIsEmpty """
        return strval is None or 0 == len(strval)

    @classmethod
    def NormalizeString(cls, strval):
        """ generated source for method NormalizeString """
        return strval if strval is not None else ""

    @classmethod
    def StringCompare(cls, lhs, rhs):
        """ generated source for method StringCompare """
        return cmp(cls.NormalizeString(str(lhs)), cls.NormalizeString(str(rhs)))

    @classmethod
    def StringCompareIgnCase(cls, lhs, rhs):
        """ generated source for method StringCompareIgnCase """
        return cmp(cls.NormalizeString(str(lhs)).lower(), cls.NormalizeString(str(rhs)).lower())

    @classmethod
    def VectorEqualsUnordered(cls, lhs, rhs):
        """ generated source for method VectorEqualsUnordered """
        if lhs == rhs:
            return True
        lhsCount = 0 if lhs is None else len(lhs)
        rhsCount = 0 if rhs is None else len(rhs)
        if lhsCount != rhsCount:
            return False
        if lhsCount == 0:
            return True
        matchedRhsElems = [bool() for __idx0 in range(rhsCount)]
        lhsIdx = 0
        while lhsIdx < lhsCount:
            lhsElem = lhs[lhsIdx]
            rhsIdx = 0
            while rhsIdx < rhsCount:
                if matchedRhsElems[rhsIdx]:
                    continue 
                if lhsElem == rhs[rhsIdx]:
                    matchedRhsElems[rhsIdx] = True
                    break
                rhsIdx += 1
            if rhsIdx >= rhsCount:
                #  no matching elem found
                return False
            lhsIdx += 1
        return True

    @classmethod
    def IntMaxString(cls, value):
        """ generated source for method IntMaxString """
        return "" if (value == Integer.MAX_VALUE) else str(value)

    @classmethod
    def DoubleMaxString(cls, value):
        """ generated source for method DoubleMaxString """
        return "" if (value == Double.MAX_VALUE) else str(value)

