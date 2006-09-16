#!/usr/bin/env python
""" Defines the ScannerSubscription class.

"""
from ib.lib import setattr_mapping, maxint, maxfloat


class ScannerSubscription(object):
    """ ScannerSubscription(...) -> scanner subscription parameters 

    """
    NO_ROW_NUMBER_SPECIFIED = -1

    
    def __init__(self,
                 numberOfRows=NO_ROW_NUMBER_SPECIFIED,
                 instrument='',
                 locationCode='',
                 scanCode='',
                 abovePrice=maxfloat,
                 belowPrice=maxfloat,
                 aboveVolume=maxint,
                 averageOptionVolumeAbove=maxint,
                 marketCapAbove=maxfloat,
                 marketCapBelow=maxfloat,
                 moodyRatingAbove='',
                 moodyRatingBelow='',
                 spRatingAbove='',
                 spRatingBelow='',
                 maturityDateAbove='',
                 maturityDateBelow='',
                 couponRateAbove=maxfloat,
                 couponRateBelow=maxfloat,
                 excludeConvertible='',
                 scannerSettingPairs='',
                 stockTypeFilter='',
                 ):
        setattr_mapping(self, locals())
