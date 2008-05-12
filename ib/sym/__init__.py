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


class UseRTH:
    no, yes = 0, 1


class ServerLogLevel:
    system, error, warning, information, detail = \
            sys, err, warn, info, det = range(1, 6)

class FaDataType:
    groups, profile, account_aliases = range(1, 4)


class ExerciseAction:
    exercise, lapse = range(1, 3)


class Override:
    no, yes, = 0, 1
