#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# This script is an exmple of using the (optional) ib.opt package
# instead of the regular API.
##

from time import sleep
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message


def my_account_handler(msg):
    print(msg)


def my_tick_handler(msg):
    print(msg)


if __name__ == '__main__':
    con = ibConnection()
    con.register(my_account_handler, 'UpdateAccountValue')
    con.register(my_tick_handler, message.tickSize, message.tickPrice)
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
    print('disconnected', con.disconnect())
    sleep(3)
    print('reconnected', con.reconnect())
    inner()
    sleep(3)

    print('again disconnected', con.disconnect())
