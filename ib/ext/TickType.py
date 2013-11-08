#!/usr/bin/env python
""" generated source for module TickType """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

# 
#  * TickType.java
#  *
#  
# package: com.ib.client
class TickType(object):
    """ generated source for class TickType """
    #  constants - tick types
    BID_SIZE = 0
    BID = 1
    ASK = 2
    ASK_SIZE = 3
    LAST = 4
    LAST_SIZE = 5
    HIGH = 6
    LOW = 7
    VOLUME = 8
    CLOSE = 9
    BID_OPTION = 10
    ASK_OPTION = 11
    LAST_OPTION = 12
    MODEL_OPTION = 13
    OPEN = 14
    LOW_13_WEEK = 15
    HIGH_13_WEEK = 16
    LOW_26_WEEK = 17
    HIGH_26_WEEK = 18
    LOW_52_WEEK = 19
    HIGH_52_WEEK = 20
    AVG_VOLUME = 21
    OPEN_INTEREST = 22
    OPTION_HISTORICAL_VOL = 23
    OPTION_IMPLIED_VOL = 24
    OPTION_BID_EXCH = 25
    OPTION_ASK_EXCH = 26
    OPTION_CALL_OPEN_INTEREST = 27
    OPTION_PUT_OPEN_INTEREST = 28
    OPTION_CALL_VOLUME = 29
    OPTION_PUT_VOLUME = 30
    INDEX_FUTURE_PREMIUM = 31
    BID_EXCH = 32
    ASK_EXCH = 33
    AUCTION_VOLUME = 34
    AUCTION_PRICE = 35
    AUCTION_IMBALANCE = 36
    MARK_PRICE = 37
    BID_EFP_COMPUTATION = 38
    ASK_EFP_COMPUTATION = 39
    LAST_EFP_COMPUTATION = 40
    OPEN_EFP_COMPUTATION = 41
    HIGH_EFP_COMPUTATION = 42
    LOW_EFP_COMPUTATION = 43
    CLOSE_EFP_COMPUTATION = 44
    LAST_TIMESTAMP = 45
    SHORTABLE = 46
    FUNDAMENTAL_RATIOS = 47
    RT_VOLUME = 48
    HALTED = 49
    BID_YIELD = 50
    ASK_YIELD = 51
    LAST_YIELD = 52
    CUST_OPTION_COMPUTATION = 53
    TRADE_COUNT = 54
    TRADE_RATE = 55
    VOLUME_RATE = 56
    LAST_RTH_TRADE = 57
    REGULATORY_IMBALANCE = 61

    @classmethod
    def getField(cls, tickType):
        """ generated source for method getField """
        if tickType == cls.BID_SIZE:
            return "bidSize"
        elif tickType == cls.BID:
            return "bidPrice"
        elif tickType == cls.ASK:
            return "askPrice"
        elif tickType == cls.ASK_SIZE:
            return "askSize"
        elif tickType == cls.LAST:
            return "lastPrice"
        elif tickType == cls.LAST_SIZE:
            return "lastSize"
        elif tickType == cls.HIGH:
            return "high"
        elif tickType == cls.LOW:
            return "low"
        elif tickType == cls.VOLUME:
            return "volume"
        elif tickType == cls.CLOSE:
            return "close"
        elif tickType == cls.BID_OPTION:
            return "bidOptComp"
        elif tickType == cls.ASK_OPTION:
            return "askOptComp"
        elif tickType == cls.LAST_OPTION:
            return "lastOptComp"
        elif tickType == cls.MODEL_OPTION:
            return "modelOptComp"
        elif tickType == cls.OPEN:
            return "open"
        elif tickType == cls.LOW_13_WEEK:
            return "13WeekLow"
        elif tickType == cls.HIGH_13_WEEK:
            return "13WeekHigh"
        elif tickType == cls.LOW_26_WEEK:
            return "26WeekLow"
        elif tickType == cls.HIGH_26_WEEK:
            return "26WeekHigh"
        elif tickType == cls.LOW_52_WEEK:
            return "52WeekLow"
        elif tickType == cls.HIGH_52_WEEK:
            return "52WeekHigh"
        elif tickType == cls.AVG_VOLUME:
            return "AvgVolume"
        elif tickType == cls.OPEN_INTEREST:
            return "OpenInterest"
        elif tickType == cls.OPTION_HISTORICAL_VOL:
            return "OptionHistoricalVolatility"
        elif tickType == cls.OPTION_IMPLIED_VOL:
            return "OptionImpliedVolatility"
        elif tickType == cls.OPTION_BID_EXCH:
            return "OptionBidExchStr"
        elif tickType == cls.OPTION_ASK_EXCH:
            return "OptionAskExchStr"
        elif tickType == cls.OPTION_CALL_OPEN_INTEREST:
            return "OptionCallOpenInterest"
        elif tickType == cls.OPTION_PUT_OPEN_INTEREST:
            return "OptionPutOpenInterest"
        elif tickType == cls.OPTION_CALL_VOLUME:
            return "OptionCallVolume"
        elif tickType == cls.OPTION_PUT_VOLUME:
            return "OptionPutVolume"
        elif tickType == cls.INDEX_FUTURE_PREMIUM:
            return "IndexFuturePremium"
        elif tickType == cls.BID_EXCH:
            return "bidExch"
        elif tickType == cls.ASK_EXCH:
            return "askExch"
        elif tickType == cls.AUCTION_VOLUME:
            return "auctionVolume"
        elif tickType == cls.AUCTION_PRICE:
            return "auctionPrice"
        elif tickType == cls.AUCTION_IMBALANCE:
            return "auctionImbalance"
        elif tickType == cls.MARK_PRICE:
            return "markPrice"
        elif tickType == cls.BID_EFP_COMPUTATION:
            return "bidEFP"
        elif tickType == cls.ASK_EFP_COMPUTATION:
            return "askEFP"
        elif tickType == cls.LAST_EFP_COMPUTATION:
            return "lastEFP"
        elif tickType == cls.OPEN_EFP_COMPUTATION:
            return "openEFP"
        elif tickType == cls.HIGH_EFP_COMPUTATION:
            return "highEFP"
        elif tickType == cls.LOW_EFP_COMPUTATION:
            return "lowEFP"
        elif tickType == cls.CLOSE_EFP_COMPUTATION:
            return "closeEFP"
        elif tickType == cls.LAST_TIMESTAMP:
            return "lastTimestamp"
        elif tickType == cls.SHORTABLE:
            return "shortable"
        elif tickType == cls.FUNDAMENTAL_RATIOS:
            return "fundamentals"
        elif tickType == cls.RT_VOLUME:
            return "RTVolume"
        elif tickType == cls.HALTED:
            return "halted"
        elif tickType == cls.BID_YIELD:
            return "bidYield"
        elif tickType == cls.ASK_YIELD:
            return "askYield"
        elif tickType == cls.LAST_YIELD:
            return "lastYield"
        elif tickType == cls.CUST_OPTION_COMPUTATION:
            return "custOptComp"
        elif tickType == cls.TRADE_COUNT:
            return "trades"
        elif tickType == cls.TRADE_RATE:
            return "trades/min"
        elif tickType == cls.VOLUME_RATE:
            return "volume/min"
        elif tickType == cls.LAST_RTH_TRADE:
            return "lastRTHTrade"
        elif tickType == cls.REGULATORY_IMBALANCE:
            return "regulatoryImbalance"
        else:
            return "unknown"

