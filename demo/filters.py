#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# This script is an exmple of using the ib.opt.messagetools module.
##

from time import sleep
from ib.ext.Contract import Contract
from ib.ext.TickType import TickType
from ib.opt import ibConnection, message
from ib.opt import messagetools

all_messages = []

def my_account_handler(msg):
    all_messages.append(msg)
    print msg



def my_tick_handler(msg):
    all_messages.append(msg)
    print msg


# wrap our tick handler to get only bid size
tick_handler = messagetools.messageFilter(my_tick_handler, lambda m:m.field==TickType.BID_SIZE)


# another way to do it
tick_handler = messagetools.bidSizeFilter(my_tick_handler)


# wrap our account handler to get only cash values
cash_handler = messagetools.messageFilter(my_account_handler, lambda m:m.key.lower().count('cash'))


# try out the new before and after send messages
def pre_req_account_updates(msg):
    all_messages.append(msg)
    print 'pre account updates: ', msg
    return True

def post_req_account_updates(msg):
    all_messages.append(msg)
    print 'post account updates: ', msg


if __name__ == '__main__':
    con = ibConnection()
    #con.enableLogging()
    con.register(cash_handler, 'UpdateAccountValue')
    con.register(tick_handler, message.tickSize, message.tickPrice)
    con.register(pre_req_account_updates, 'ReqAccountUpdatesPre')
    con.register(post_req_account_updates, 'PostReqAccountUpdatesPost')
    con.connect()

    def inner():
        con.reqAccountUpdates(1, '')
        qqqq = Contract()
        qqqq.m_symbol = 'QQQQ'
        qqqq.m_secType = 'STK'
        qqqq.m_exchange = 'SMART'
        con.reqMktData(1, qqqq, '', False)

    inner()
    sleep(5)
