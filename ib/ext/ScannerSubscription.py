#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

    def get_couponRateBelow(self):
        return self.m_couponRateBelow

    def set_couponRateBelow(self, r):
        self.m_couponRateBelow = r

    couponRateBelow = property(get_couponRateBelow, set_couponRateBelow)

    def get_scannerSettingPairs(self):
        return self.m_scannerSettingPairs

    def set_scannerSettingPairs(self, val):
        self.m_scannerSettingPairs = val

    scannerSettingPairs = property(get_scannerSettingPairs, set_scannerSettingPairs)

    def get_maturityDateBelow(self):
        return self.m_maturityDateBelow

    def set_maturityDateBelow(self, d):
        self.m_maturityDateBelow = d

    maturityDateBelow = property(get_maturityDateBelow, set_maturityDateBelow)

    def get_spRatingBelow(self):
        return self.m_spRatingBelow

    def set_spRatingBelow(self, r):
        self.m_spRatingBelow = r

    spRatingBelow = property(get_spRatingBelow, set_spRatingBelow)

    def get_averageOptionVolumeAbove(self):
        return self.m_averageOptionVolumeAbove

    def set_averageOptionVolumeAbove(self, volume):
        self.m_averageOptionVolumeAbove = volume

    averageOptionVolumeAbove = property(get_averageOptionVolumeAbove, set_averageOptionVolumeAbove)

    def get_scanCode(self):
        return self.m_scanCode

    def set_scanCode(self, txt):
        self.m_scanCode = txt

    scanCode = property(get_scanCode, set_scanCode)

    def get_marketCapBelow(self):
        return self.m_marketCapBelow

    def set_marketCapBelow(self, cap):
        self.m_marketCapBelow = cap

    marketCapBelow = property(get_marketCapBelow, set_marketCapBelow)

    def get_aboveVolume(self):
        return self.m_aboveVolume

    def set_aboveVolume(self, volume):
        self.m_aboveVolume = volume

    aboveVolume = property(get_aboveVolume, set_aboveVolume)

    def get_stockTypeFilter(self):
        return self.m_stockTypeFilter

    def set_stockTypeFilter(self, val):
        self.m_stockTypeFilter = val

    stockTypeFilter = property(get_stockTypeFilter, set_stockTypeFilter)

    def get_moodyRatingAbove(self):
        return self.m_moodyRatingAbove

    def set_moodyRatingAbove(self, r):
        self.m_moodyRatingAbove = r

    moodyRatingAbove = property(get_moodyRatingAbove, set_moodyRatingAbove)

    def get_marketCapAbove(self):
        return self.m_marketCapAbove

    def set_marketCapAbove(self, cap):
        self.m_marketCapAbove = cap

    marketCapAbove = property(get_marketCapAbove, set_marketCapAbove)

    def get_numberOfRows(self):
        return self.m_numberOfRows

    def set_numberOfRows(self, num):
        self.m_numberOfRows = num

    numberOfRows = property(get_numberOfRows, set_numberOfRows)

    def get_abovePrice(self):
        return self.m_abovePrice

    def set_abovePrice(self, price):
        self.m_abovePrice = price

    abovePrice = property(get_abovePrice, set_abovePrice)

    def get_instrument(self):
        return self.m_instrument

    def set_instrument(self, txt):
        self.m_instrument = txt

    instrument = property(get_instrument, set_instrument)

    def get_belowPrice(self):
        return self.m_belowPrice

    def set_belowPrice(self, price):
        self.m_belowPrice = price

    belowPrice = property(get_belowPrice, set_belowPrice)

    def get_excludeConvertible(self):
        return self.m_excludeConvertible

    def set_excludeConvertible(self, c):
        self.m_excludeConvertible = c

    excludeConvertible = property(get_excludeConvertible, set_excludeConvertible)

    def get_couponRateAbove(self):
        return self.m_couponRateAbove

    def set_couponRateAbove(self, r):
        self.m_couponRateAbove = r

    couponRateAbove = property(get_couponRateAbove, set_couponRateAbove)

    def get_moodyRatingBelow(self):
        return self.m_moodyRatingBelow

    def set_moodyRatingBelow(self, r):
        self.m_moodyRatingBelow = r

    moodyRatingBelow = property(get_moodyRatingBelow, set_moodyRatingBelow)

    def get_spRatingAbove(self):
        return self.m_spRatingAbove

    def set_spRatingAbove(self, r):
        self.m_spRatingAbove = r

    spRatingAbove = property(get_spRatingAbove, set_spRatingAbove)

    def get_maturityDateAbove(self):
        return self.m_maturityDateAbove

    def set_maturityDateAbove(self, d):
        self.m_maturityDateAbove = d

    maturityDateAbove = property(get_maturityDateAbove, set_maturityDateAbove)

    def get_locationCode(self):
        return self.m_locationCode

    def set_locationCode(self, txt):
        self.m_locationCode = txt

    locationCode = property(get_locationCode, set_locationCode)

