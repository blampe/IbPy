#!/usr/bin/env python
# -*- coding: utf-8 -*-


def durationMethod(k):
    def m(cls, val):
        return '%s %s' % (val, k)
    return classmethod(m)


class HDDuration:
    seconds = durationMethod('S')
    days = durationMethod('D')
    weeks = durationMethod('W')
    months = durationMethod('M')
    years = durationMethod('Y')


class HDBar:
    sec = sec1 = '1 sec'
    sec5 = '5 secs'
    sec15 = '15 secs'
    sec30 = '30 secs'
    min1 = '1 min'
    min2 = '2 mins'
    min5 = '5 mins'
    min15 = '15 mins'
    min30 = '30 mins'
    hour = hour1 = '1 hour'
    day = day1 = '1 day'
    week = week1 = '1 week'
    month = month1 = '1 month'
    month3 = '3 months'
    year = year1 = '1 year'


class HDShow:
    trades = 'TRADES'
    mid = 'MIDPOINT'
    bid = 'BID'
    ask = 'ASK'
    bid_ask = 'BID/ASK'

class HDDateFormat:
    long = 1 # yyyymmdd{space}{space}hh:mm:dd
    short = 2 # 1/1/1970 GMT


class YesNo:
    no = false = 0
    yes = true = 1


class RTH(YesNo):
    pass


class AllOrNone(YesNo):
    pass

class Override(YesNo):
    pass

class FirmQuoteOnly(YesNo):
    pass

class ETradeOnly(YesNo):
    pass

class ContinuousUpdate(YesNo):
    pass


class AuctionStrategy:
    match = 1
    improvement = 2
    transparent = 3

class ServerLogLevel:
    system, error, warning, information, detail = \
            sys, err, warn, info, det = range(1, 6)


class FaDataType:
    groups, profile, account_aliases = range(1, 4)


class ExerciseAction:
    exercise, lapse = range(1, 3)


class TriggerMethod:
    default = 0
    double_askbid = 1
    last = 2
    double_last = 3


class ShortSaleSlot:
    unapplicable = 0
    clearing_broker = 1
    third_party = 2


class OcaType:
    cancel_on_fill_block = 1
    reduce_on_fill_block = 2
    reduce_on_fill_noblock = 3


class Rule80a:
    individual = 'I'
    agency = 'A'
    agent_other_member = 'W'
    individual_ptia = 'J'
    agency_ptia = 'U'
    agent_other_member_ptia = 'M'
    individual_pt = 'K'
    agency_pt = 'Y'
    agent_other_member_pt = 'N'


class RefPriceType:
    avg = 1
    bidask = 2

class VolatilityType:
    daily = 1
    annual = 2


class GenericTickTypes:
    option_volume = 100
    option_open_interest = 101
    historical_volatility = 104
    option_implied_volatility = 106
    index_future_premium = 162
    misc_stats = 165
    mark_price = 221
    auction_values = 225
    shortable = 236


class TickValues:
    low_13_week = 15
    high_13_week = 16
    low_26_week = 17
    high_26_week = 18
    low_52_week = 19
    high_52_week = 20
    avg_volume = 21
    option_historical_vol = 23
    option_implied_vol = 24
    option_call_open_interest = 27
    option_put_open_interest = 28
    option_call_volume = 29
    option_put_volume = 30
    index_future_premium = 31
    auction_volume = 34
    auction_price = 35
    auction_imbalance = 36
    mark_price = 37
    shortable = 46
