#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep


def watcher(msg):
    print msg


def makeStkContract(sym):
    newStkContract = Contract()
    newStkContract.m_symbol = sym
    newStkContract.m_secType = 'CASH'
    newStkContract.m_strike = 0.00
    newStkContract.m_exchange = 'IDEALPRO'
    newStkContract.m_currency = 'USD'
    return newStkContract


def makeOptContract(sym, exp, right, strike):
    newOptContract = Contract()
    newOptContract.m_symbol = sym
    newOptContract.m_secType = 'OPT'
    newOptContract.m_right = right
    newOptContract.m_expiry = exp
    newOptContract.m_strike = float(strike)
    newOptContract.m_exchange = 'SMART'
    newOptContract.m_currency = 'USD'
    #newOptContract.m_localSymbol = ''
    #newOptContract.m_primaryExch = ''
    return newOptContract


def makeOptOrder(action, orderID, tif, orderType):
    newOptOrder = Order()
    newOptOrder.m_orderId = orderID
    newOptOrder.m_clientId = 0
    newOptOrder.m_permid = 0
    newOptOrder.m_action = action
    newOptOrder.m_lmtPrice = 0
    newOptOrder.m_auxPrice = 0
    newOptOrder.m_tif = tif
    newOptOrder.m_transmit = False
    newOptOrder.m_orderType = orderType
    newOptOrder.m_totalQuantity = 1
    return newOptOrder


if __name__ == '__main__':
    con = ibConnection()
    con.registerAll(watcher)
    con.connect()

    tickID = 36
    orderID = -100 #50002 + 10

    stkContract = makeStkContract('EUR')
    con.reqMktData(1, stkContract, '', '')

    optContract = makeOptContract('QQQQ', '20080919', 'C', 34.0)
    con.reqMktData(tickID, optContract, '', '')
    #sleep(5)
    #con.cancelMktData(tickID)
    #sleep(5)
    optOrder = makeOptOrder( 'BUY', orderID, 'DAY', 'MKT')
    con.placeOrder(orderID, optContract, optOrder)


    print con.reqMktData(tickID, optContract, '', False)

    sleep(5)
    con.disconnect()
    sleep(1)
