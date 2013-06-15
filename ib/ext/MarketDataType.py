#!/usr/bin/env python
""" generated source for module MarketDataType """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

# 
#  * MarketDataType.java
#  *
#  
# package: com.ib.client
class MarketDataType(object):
    """ generated source for class MarketDataType """
    #  constants - market data types
    REALTIME = 1
    FROZEN = 2

    @classmethod
    def getField(cls, marketDataType):
        """ generated source for method getField """
        if marketDataType==cls.REALTIME:
            return "Real-Time"
        elif marketDataType==cls.FROZEN:
            return "Frozen"
        else:
            return "Unknown"

    @classmethod
    def getFields(cls):
        """ generated source for method getFields """
        totalFields = 2
        fields = [None]*totalFields
        i = 0
        while i < totalFields:
            fields[i] = MarketDataType.getField(i + 1)
            i += 1
        return fields

