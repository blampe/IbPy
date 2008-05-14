#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for ScannerSubscription.
##

# Source file: ScannerSubscription.java
# Target file: ScannerSubscription.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib import Double, Integer
from ib.lib.overloading import overloaded

class ScannerSubscription(object):
    """ generated source for ScannerSubscription

    """
    NO_ROW_NUMBER_SPECIFIED = -1
    m_numberOfRows = NO_ROW_NUMBER_SPECIFIED
    m_instrument = ""
    m_locationCode = ""
    m_scanCode = ""
    m_abovePrice = Double.MAX_VALUE
    m_belowPrice = Double.MAX_VALUE
    m_aboveVolume = Integer.MAX_VALUE
    m_averageOptionVolumeAbove = Integer.MAX_VALUE
    m_marketCapAbove = Double.MAX_VALUE
    m_marketCapBelow = Double.MAX_VALUE
    m_moodyRatingAbove = ""
    m_moodyRatingBelow = ""
    m_spRatingAbove = ""
    m_spRatingBelow = ""
    m_maturityDateAbove = ""
    m_maturityDateBelow = ""
    m_couponRateAbove = Double.MAX_VALUE
    m_couponRateBelow = Double.MAX_VALUE
    m_excludeConvertible = ""
    m_scannerSettingPairs = ""
    m_stockTypeFilter = ""

    @overloaded
    def numberOfRows(self):
        return self.m_numberOfRows

    @overloaded
    def instrument(self):
        return self.m_instrument

    @overloaded
    def locationCode(self):
        return self.m_locationCode

    @overloaded
    def scanCode(self):
        return self.m_scanCode

    @overloaded
    def abovePrice(self):
        return self.m_abovePrice

    @overloaded
    def belowPrice(self):
        return self.m_belowPrice

    @overloaded
    def aboveVolume(self):
        return self.m_aboveVolume

    @overloaded
    def averageOptionVolumeAbove(self):
        return self.m_averageOptionVolumeAbove

    @overloaded
    def marketCapAbove(self):
        return self.m_marketCapAbove

    @overloaded
    def marketCapBelow(self):
        return self.m_marketCapBelow

    @overloaded
    def moodyRatingAbove(self):
        return self.m_moodyRatingAbove

    @overloaded
    def moodyRatingBelow(self):
        return self.m_moodyRatingBelow

    @overloaded
    def spRatingAbove(self):
        return self.m_spRatingAbove

    @overloaded
    def spRatingBelow(self):
        return self.m_spRatingBelow

    @overloaded
    def maturityDateAbove(self):
        return self.m_maturityDateAbove

    @overloaded
    def maturityDateBelow(self):
        return self.m_maturityDateBelow

    @overloaded
    def couponRateAbove(self):
        return self.m_couponRateAbove

    @overloaded
    def couponRateBelow(self):
        return self.m_couponRateBelow

    @overloaded
    def excludeConvertible(self):
        return self.m_excludeConvertible

    @overloaded
    def scannerSettingPairs(self):
        return self.m_scannerSettingPairs

    @overloaded
    def stockTypeFilter(self):
        return self.m_stockTypeFilter

    @numberOfRows.register(object, int)
    def numberOfRows_0(self, num):
        self.m_numberOfRows = num

    @instrument.register(object, str)
    def instrument_0(self, txt):
        self.m_instrument = txt

    @locationCode.register(object, str)
    def locationCode_0(self, txt):
        self.m_locationCode = txt

    @scanCode.register(object, str)
    def scanCode_0(self, txt):
        self.m_scanCode = txt

    @abovePrice.register(object, float)
    def abovePrice_0(self, price):
        self.m_abovePrice = price

    @belowPrice.register(object, float)
    def belowPrice_0(self, price):
        self.m_belowPrice = price

    @aboveVolume.register(object, int)
    def aboveVolume_0(self, volume):
        self.m_aboveVolume = volume

    @averageOptionVolumeAbove.register(object, int)
    def averageOptionVolumeAbove_0(self, volume):
        self.m_averageOptionVolumeAbove = volume

    @marketCapAbove.register(object, float)
    def marketCapAbove_0(self, cap):
        self.m_marketCapAbove = cap

    @marketCapBelow.register(object, float)
    def marketCapBelow_0(self, cap):
        self.m_marketCapBelow = cap

    @moodyRatingAbove.register(object, str)
    def moodyRatingAbove_0(self, r):
        self.m_moodyRatingAbove = r

    @moodyRatingBelow.register(object, str)
    def moodyRatingBelow_0(self, r):
        self.m_moodyRatingBelow = r

    @spRatingAbove.register(object, str)
    def spRatingAbove_0(self, r):
        self.m_spRatingAbove = r

    @spRatingBelow.register(object, str)
    def spRatingBelow_0(self, r):
        self.m_spRatingBelow = r

    @maturityDateAbove.register(object, str)
    def maturityDateAbove_0(self, d):
        self.m_maturityDateAbove = d

    @maturityDateBelow.register(object, str)
    def maturityDateBelow_0(self, d):
        self.m_maturityDateBelow = d

    @couponRateAbove.register(object, float)
    def couponRateAbove_0(self, r):
        self.m_couponRateAbove = r

    @couponRateBelow.register(object, float)
    def couponRateBelow_0(self, r):
        self.m_couponRateBelow = r

    @excludeConvertible.register(object, str)
    def excludeConvertible_0(self, c):
        self.m_excludeConvertible = c

    @scannerSettingPairs.register(object, str)
    def scannerSettingPairs_0(self, val):
        self.m_scannerSettingPairs = val

    @stockTypeFilter.register(object, str)
    def stockTypeFilter_0(self, val):
        self.m_stockTypeFilter = val


