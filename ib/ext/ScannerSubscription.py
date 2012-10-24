#!/usr/bin/env python
""" generated source for module ScannerSubscription """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib import Double, Integer
from ib.lib.overloading import overloaded
# package: com.ib.client
class ScannerSubscription(object):
    """ generated source for class ScannerSubscription """
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

    #  Get
    @overloaded
    def numberOfRows(self):
        """ generated source for method numberOfRows """
        return self.m_numberOfRows

    @overloaded
    def instrument(self):
        """ generated source for method instrument """
        return self.m_instrument

    @overloaded
    def locationCode(self):
        """ generated source for method locationCode """
        return self.m_locationCode

    @overloaded
    def scanCode(self):
        """ generated source for method scanCode """
        return self.m_scanCode

    @overloaded
    def abovePrice(self):
        """ generated source for method abovePrice """
        return self.m_abovePrice

    @overloaded
    def belowPrice(self):
        """ generated source for method belowPrice """
        return self.m_belowPrice

    @overloaded
    def aboveVolume(self):
        """ generated source for method aboveVolume """
        return self.m_aboveVolume

    @overloaded
    def averageOptionVolumeAbove(self):
        """ generated source for method averageOptionVolumeAbove """
        return self.m_averageOptionVolumeAbove

    @overloaded
    def marketCapAbove(self):
        """ generated source for method marketCapAbove """
        return self.m_marketCapAbove

    @overloaded
    def marketCapBelow(self):
        """ generated source for method marketCapBelow """
        return self.m_marketCapBelow

    @overloaded
    def moodyRatingAbove(self):
        """ generated source for method moodyRatingAbove """
        return self.m_moodyRatingAbove

    @overloaded
    def moodyRatingBelow(self):
        """ generated source for method moodyRatingBelow """
        return self.m_moodyRatingBelow

    @overloaded
    def spRatingAbove(self):
        """ generated source for method spRatingAbove """
        return self.m_spRatingAbove

    @overloaded
    def spRatingBelow(self):
        """ generated source for method spRatingBelow """
        return self.m_spRatingBelow

    @overloaded
    def maturityDateAbove(self):
        """ generated source for method maturityDateAbove """
        return self.m_maturityDateAbove

    @overloaded
    def maturityDateBelow(self):
        """ generated source for method maturityDateBelow """
        return self.m_maturityDateBelow

    @overloaded
    def couponRateAbove(self):
        """ generated source for method couponRateAbove """
        return self.m_couponRateAbove

    @overloaded
    def couponRateBelow(self):
        """ generated source for method couponRateBelow """
        return self.m_couponRateBelow

    @overloaded
    def excludeConvertible(self):
        """ generated source for method excludeConvertible """
        return self.m_excludeConvertible

    @overloaded
    def scannerSettingPairs(self):
        """ generated source for method scannerSettingPairs """
        return self.m_scannerSettingPairs

    @overloaded
    def stockTypeFilter(self):
        """ generated source for method stockTypeFilter """
        return self.m_stockTypeFilter

    #  Set
    @numberOfRows.register(object, int)
    def numberOfRows_0(self, num):
        """ generated source for method numberOfRows_0 """
        self.m_numberOfRows = num

    @instrument.register(object, str)
    def instrument_0(self, txt):
        """ generated source for method instrument_0 """
        self.m_instrument = txt

    @locationCode.register(object, str)
    def locationCode_0(self, txt):
        """ generated source for method locationCode_0 """
        self.m_locationCode = txt

    @scanCode.register(object, str)
    def scanCode_0(self, txt):
        """ generated source for method scanCode_0 """
        self.m_scanCode = txt

    @abovePrice.register(object, float)
    def abovePrice_0(self, price):
        """ generated source for method abovePrice_0 """
        self.m_abovePrice = price

    @belowPrice.register(object, float)
    def belowPrice_0(self, price):
        """ generated source for method belowPrice_0 """
        self.m_belowPrice = price

    @aboveVolume.register(object, int)
    def aboveVolume_0(self, volume):
        """ generated source for method aboveVolume_0 """
        self.m_aboveVolume = volume

    @averageOptionVolumeAbove.register(object, int)
    def averageOptionVolumeAbove_0(self, volume):
        """ generated source for method averageOptionVolumeAbove_0 """
        self.m_averageOptionVolumeAbove = volume

    @marketCapAbove.register(object, float)
    def marketCapAbove_0(self, cap):
        """ generated source for method marketCapAbove_0 """
        self.m_marketCapAbove = cap

    @marketCapBelow.register(object, float)
    def marketCapBelow_0(self, cap):
        """ generated source for method marketCapBelow_0 """
        self.m_marketCapBelow = cap

    @moodyRatingAbove.register(object, str)
    def moodyRatingAbove_0(self, r):
        """ generated source for method moodyRatingAbove_0 """
        self.m_moodyRatingAbove = r

    @moodyRatingBelow.register(object, str)
    def moodyRatingBelow_0(self, r):
        """ generated source for method moodyRatingBelow_0 """
        self.m_moodyRatingBelow = r

    @spRatingAbove.register(object, str)
    def spRatingAbove_0(self, r):
        """ generated source for method spRatingAbove_0 """
        self.m_spRatingAbove = r

    @spRatingBelow.register(object, str)
    def spRatingBelow_0(self, r):
        """ generated source for method spRatingBelow_0 """
        self.m_spRatingBelow = r

    @maturityDateAbove.register(object, str)
    def maturityDateAbove_0(self, d):
        """ generated source for method maturityDateAbove_0 """
        self.m_maturityDateAbove = d

    @maturityDateBelow.register(object, str)
    def maturityDateBelow_0(self, d):
        """ generated source for method maturityDateBelow_0 """
        self.m_maturityDateBelow = d

    @couponRateAbove.register(object, float)
    def couponRateAbove_0(self, r):
        """ generated source for method couponRateAbove_0 """
        self.m_couponRateAbove = r

    @couponRateBelow.register(object, float)
    def couponRateBelow_0(self, r):
        """ generated source for method couponRateBelow_0 """
        self.m_couponRateBelow = r

    @excludeConvertible.register(object, str)
    def excludeConvertible_0(self, c):
        """ generated source for method excludeConvertible_0 """
        self.m_excludeConvertible = c

    @scannerSettingPairs.register(object, str)
    def scannerSettingPairs_0(self, val):
        """ generated source for method scannerSettingPairs_0 """
        self.m_scannerSettingPairs = val

    @stockTypeFilter.register(object, str)
    def stockTypeFilter_0(self, val):
        """ generated source for method stockTypeFilter_0 """
        self.m_stockTypeFilter = val

