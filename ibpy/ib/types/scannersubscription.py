#!/usr/bin/env python
""" Defines the ScannerSubscription class.

"""
from ib.lib import setattr_mapping


class ScannerSubscription(object):
    """ ScannerSubscription(...) -> scanner subscription parameters 

    """
    dblmax= ''
    intmax = ''
    def __init__(self,
                 numberOfRows=-1,
                 instrument='',
                 locationCode='',
                 scanCode='',
                 abovePrice=dblmax,
                 belowPrice=dblmax,
                 aboveVolume=intmax,
                 averageOptionVolumeAbove=intmax,
                 marketCapAbove=dblmax,
                 marketCapBelow=dblmax,                 
                 moodyRatingAbove='',
                 moodyRatingBelow='',
                 spRatingAbove='',
                 spRatingBelow='',
                 maturityDateAbove='',
                 maturityDateBelow='',
                 couponRateAbove=dblmax,
                 couponRateBelow=dblmax,
                 excludeConvertible=0,
                 scannerSettingPairs='',
                 stockTypeFilter=''):
        setattr_mapping(self, locals())
