#!/usr/bin/env python
""" Defines the ScannerSubscription class.

"""
from ib.lib import setattr_mapping


class ScannerSubscription(object):
    """ ScannerSubscription(...) -> scanner subscription parameters 

    """
    doubleMax= ''
    integerMax = ''


    def __init__(self,
                 numberOfRows=-1,
                 instrument='',
                 locationCode='',
                 scanCode='',
                 abovePrice=doubleMax,
                 belowPrice=doubleMax,
                 aboveVolume=integerMax,
                 averageOptionVolumeAbove=integerMax,
                 marketCapAbove=doubleMax,
                 marketCapBelow=doubleMax,                 
                 moodyRatingAbove='',
                 moodyRatingBelow='',
                 spRatingAbove='',
                 spRatingBelow='',
                 maturityDateAbove='',
                 maturityDateBelow='',
                 couponRateAbove=doubleMax,
                 couponRateBelow=doubleMax,
                 excludeConvertible='',
                 scannerSettingPairs='',
                 stockTypeFilter=''):
        setattr_mapping(self, locals())
