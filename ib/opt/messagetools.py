#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial, wraps

from ib.ext.TickType import TickType


##
# To programmatically generate the TickType filters, use something like this sketch:
#
# vs = [(name, value) for name, value in [(name, getattr(TickType, name))
#                                         for name in dir(TickType)] if type(value)==int]
# titlevalues = [(title[0].lower()+title[1:], value)
#                for title in [''.join([part.title() for part in name.split('_')])
#                              for name, value in vs]]


def messageFilter(function, predicate=lambda msg:True):
    @wraps(function)
    def inner(msg):
        if predicate(msg):
            return function(msg)
    return inner


askSizeFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickType.ASK_SIZE)
askPriceFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickType.ASK)

bidSizeFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickType.BID_SIZE)
bidPriceFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickType.BID)

lastSizeFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickType.LAST_SIZE)
lastPriceFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickType.LAST)


# We don't need functions for filtering by message type because that's
# what the reader/receiver/dispatcher already does.
