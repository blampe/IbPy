#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for Contract.
##

# Source file: Contract.java
# Target file: Contract.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes made to this file will be lost.

from ib.lib.overloading import overloaded
from ib.lib import Cloneable

class Contract(Cloneable):
    """ generated source for Contract

    """
    m_symbol = ""
    m_secType = ""
    m_expiry = ""
    m_strike = float()
    m_right = ""
    m_multiplier = ""
    m_exchange = ""
    m_currency = ""
    m_localSymbol = ""
    m_primaryExch = ""
    m_includeExpired = bool()
    m_comboLegsDescrip = ""
    m_comboLegs = []
    m_cusip = ""
    m_ratings = ""
    m_descAppend = ""
    m_bondType = ""
    m_couponType = ""
    m_callable = bool()
    m_putable = bool()
    m_coupon = float()
    m_convertible = bool()
    m_maturity = ""
    m_issueDate = ""
    m_nextOptionDate = ""
    m_nextOptionType = ""
    m_nextOptionPartial = bool()
    m_notes = ""

    @overloaded
    def __init__(self):
        self.m_strike = 0

    def clone(self):
        retval = super.clone()
        retval.m_comboLegs = retval.m_comboLegs.clone()
        return retval

    @__init__.register(object, str, str, str, float, str, str, str, str, str, list, str, bool, str, str, str, str, str, bool, bool, float, bool, str, str, str, str, bool, str)
    def __init___0(self, p_symbol,
                         p_secType,
                         p_expiry,
                         p_strike,
                         p_right,
                         p_multiplier,
                         p_exchange,
                         p_currency,
                         p_localSymbol,
                         p_comboLegs,
                         p_primaryExch,
                         p_includeExpired,
                         p_cusip,
                         p_ratings,
                         p_descAppend,
                         p_bondType,
                         p_couponType,
                         p_callable,
                         p_putable,
                         p_coupon,
                         p_convertible,
                         p_maturity,
                         p_issueDate,
                         p_nextOptionDate,
                         p_nextOptionType,
                         p_nextOptionPartial,
                         p_notes):
        self.m_symbol = p_symbol
        self.m_secType = p_secType
        self.m_expiry = p_expiry
        self.m_strike = p_strike
        self.m_right = p_right
        self.m_multiplier = p_multiplier
        self.m_exchange = p_exchange
        self.m_currency = p_currency
        self.m_includeExpired = p_includeExpired
        self.m_localSymbol = p_localSymbol
        self.m_comboLegs = p_comboLegs
        self.m_primaryExch = p_primaryExch
        self.m_cusip = p_cusip
        self.m_ratings = p_ratings
        self.m_descAppend = p_descAppend
        self.m_bondType = p_bondType
        self.m_couponType = p_couponType
        self.m_callable = p_callable
        self.m_putable = p_putable
        self.m_coupon = p_coupon
        self.m_convertible = p_convertible
        self.m_maturity = p_maturity
        self.m_issueDate = p_issueDate
        self.m_nextOptionDate = p_nextOptionDate
        self.m_nextOptionType = p_nextOptionType
        self.m_nextOptionPartial = p_nextOptionPartial
        self.m_notes = p_notes

    def __eq__(self, p_other):
        if p_other is None or not isinstance(p_other, (Contract)) or (len(self.m_comboLegs) != len(p_other.m_comboLegs)):
            return False
        else:
            if self is p_other:
                return True
        l_theOther = p_other
        l_bContractEquals = False
        l_thisSecType = self.m_secType if self.m_secType is not None else ""
        l_otherSecType = l_theOther.m_secType if l_theOther.m_secType is not None else ""
        if not l_thisSecType == l_otherSecType:
            l_bContractEquals = False
        else:
            l_thisSymbol = self.m_symbol if self.m_symbol is not None else ""
            l_thisExchange = self.m_exchange if self.m_exchange is not None else ""
            l_thisPrimaryExch = self.m_primaryExch if self.m_primaryExch is not None else ""
            l_thisCurrency = self.m_currency if self.m_currency is not None else ""
            l_otherSymbol = l_theOther.m_symbol if l_theOther.m_symbol is not None else ""
            l_otherExchange = l_theOther.m_exchange if l_theOther.m_exchange is not None else ""
            l_otherPrimaryExch = l_theOther.m_primaryExch if l_theOther.m_primaryExch is not None else ""
            l_otherCurrency = l_theOther.m_currency if l_theOther.m_currency is not None else ""
            l_bContractEquals = l_thisSymbol == l_otherSymbol and l_thisExchange == l_otherExchange and l_thisPrimaryExch == l_otherPrimaryExch and l_thisCurrency == l_otherCurrency
            if l_bContractEquals:
                if l_thisSecType == "BOND":
                    l_bContractEquals = (self.m_putable == l_theOther.m_putable) and (self.m_callable == l_theOther.m_callable) and (self.m_convertible == l_theOther.m_convertible) and (self.m_coupon == l_theOther.m_coupon) and (self.m_nextOptionPartial == l_theOther.m_nextOptionPartial)
                    if l_bContractEquals:
                        l_thisCusip = self.m_cusip if self.m_cusip is not None else ""
                        l_thisRatings = self.m_ratings if self.m_ratings is not None else ""
                        l_thisDescAppend = self.m_descAppend if self.m_descAppend is not None else ""
                        l_thisBondType = self.m_bondType if self.m_bondType is not None else ""
                        l_thisCouponType = self.m_couponType if self.m_couponType is not None else ""
                        l_thisMaturity = self.m_maturity if self.m_maturity is not None else ""
                        l_thisIssueDate = self.m_issueDate if self.m_issueDate is not None else ""
                        l_otherCusip = l_theOther.m_cusip if l_theOther.m_cusip is not None else ""
                        l_otherRatings = l_theOther.m_ratings if l_theOther.m_ratings is not None else ""
                        l_otherDescAppend = l_theOther.m_descAppend if l_theOther.m_descAppend is not None else ""
                        l_otherBondType = l_theOther.m_bondType if l_theOther.m_bondType is not None else ""
                        l_otherCouponType = l_theOther.m_couponType if l_theOther.m_couponType is not None else ""
                        l_otherMaturity = l_theOther.m_maturity if l_theOther.m_maturity is not None else ""
                        l_otherIssueDate = l_theOther.m_issueDate if l_theOther.m_issueDate is not None else ""
                        l_otherOptionDate = l_theOther.m_nextOptionDate if l_theOther.m_nextOptionDate is not None else ""
                        l_otherOptionType = l_theOther.m_nextOptionType if l_theOther.m_nextOptionType is not None else ""
                        l_otherNotes = l_theOther.m_notes if l_theOther.m_notes is not None else ""
                        l_bContractEquals = l_thisCusip == l_otherCusip and l_thisRatings == l_otherRatings and l_thisDescAppend == l_otherDescAppend and l_thisBondType == l_otherBondType and l_thisCouponType == l_otherCouponType and l_thisMaturity == l_otherMaturity and l_thisIssueDate == l_otherIssueDate and l_otherOptionDate == l_otherOptionDate and l_otherOptionType == l_otherOptionType and l_otherNotes == l_otherNotes
                else:
                    l_thisExpiry = self.m_expiry if self.m_expiry is not None else ""
                    l_thisRight = self.m_right if self.m_right is not None else ""
                    l_thisMultiplier = self.m_multiplier if self.m_multiplier is not None else ""
                    l_thisLocalSymbol = self.m_localSymbol if self.m_localSymbol is not None else ""
                    l_otherExpiry = l_theOther.m_expiry if l_theOther.m_expiry is not None else ""
                    l_otherRight = l_theOther.m_right if l_theOther.m_right is not None else ""
                    l_otherMultiplier = l_theOther.m_multiplier if l_theOther.m_multiplier is not None else ""
                    l_otherLocalSymbol = l_theOther.m_localSymbol if l_theOther.m_localSymbol is not None else ""
                    l_bContractEquals = l_thisExpiry == l_otherExpiry and (self.m_strike == l_theOther.m_strike) and l_thisRight == l_otherRight and l_thisMultiplier == l_otherMultiplier and l_thisLocalSymbol == l_otherLocalSymbol
        if l_bContractEquals and len(self.m_comboLegs) > 0:
            alreadyMatchedSecondLeg = [bool() for __idx0 in range(len(self.m_comboLegs))]
            ## for-while
            ctr1 = 0
            while ctr1 < len(self.m_comboLegs):
                l_thisComboLeg = self.m_comboLegs[ctr1]
                l_bLegsEqual = False
                ## for-while
                ctr2 = 0
                while ctr2 < len(l_theOther.m_comboLegs):
                    if alreadyMatchedSecondLeg[ctr2]:
                        continue
                    if l_thisComboLeg == l_theOther.m_comboLegs[ctr2]:
                        l_bLegsEqual = alreadyMatchedSecondLeg[ctr2] = True
                        break
                    ctr2 += 1
                if not l_bLegsEqual:
                    return False
                ctr1 += 1
        return l_bContractEquals


