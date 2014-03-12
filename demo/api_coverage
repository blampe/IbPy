#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# This script attempts to determine how much of the TWS API is
# available from IbPy.
#
# It's not meant as an example of correct use of the package, nor is
# it an example of correct use of a programming language.
#
##
import logging
import sys

from functools import partial
from logging import DEBUG, INFO, WARN, ERROR
from optparse import OptionParser
from random import randint
from time import sleep, strftime, time

from ib.ext.ComboLeg import ComboLeg
from ib.ext.Contract import Contract
from ib.ext.ExecutionFilter import ExecutionFilter
from ib.ext.Order import Order
from ib.ext.ScannerSubscription import ScannerSubscription
from ib.lib.logger import logger as basicConfig
from ib.opt import ibConnection, message


error_msgs = {}
order_ids = [0]
tick_msgs = []
short_sleep = partial(sleep, 1)
long_sleep = partial(sleep, 10)
generic_tick_keys = '100,101,104,106,165,221,225,236'

unseen_hints = {
    'OpenOrder' : 'only works with existing order(s) before connecting',
    'RealtimeBar' : 'only works during trading hours',
    'ReceiveFA' : 'does not work with edemo account',
    'UpdateNewsBulletin' : 'news bulletins may not be available',
    'ConnectionClosed' : 'may work if TWS is closed during script',
    }

verbose_levels = {
    3 : DEBUG,
    2 : INFO,
    1 : WARN,
    0 : ERROR,
    }


def format_error(msg):
    which = ('(in %s)' % error_msgs.get(msg)) if error_msgs.get(msg) else ''
    return '%8s: %s %s' % (msg.errorCode, msg.errorMsg, which)


def format_default(msg):
    return '    %s' % msg


msg_formatters = {
    'default':format_default,
    'Error':format_error,
    }


def next_order_id():
    return order_ids[-1]


def save_order_id(msg):
    order_ids.append(msg.orderId)


def save_tick(msg):
    tick_msgs.append(msg)


def gen_tick_id():
    i = randint(100, 10000)
    while True:
        yield i
        i += 1
if sys.version_info[0] < 3:
    gen_tick_id = gen_tick_id().next
else:
    gen_tick_id = gen_tick_id().__next__


def make_contract(symbol):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = 'STK'
    contract.m_exchange = 'SMART'
    contract.m_primaryExch = 'SMART'
    contract.m_currency = 'USD'
    contract.m_localSymbol = symbol
    return contract


def make_order(limit_price):
    order = Order()
    order.m_minQty = 100
    order.m_lmtPrice = limit_price
    order.m_orderType = 'MKT'
    order.m_totalQuantity = 100
    order.m_action = 'BUY'
    return order


def exec_filter(client_id):
    contract = make_contract('NVDA')
    filt = ExecutionFilter()
    filt.m_clientId = client_id
    filt.m_symbol = contract.m_symbol
    filt.m_secType = contract.m_secType
    filt.m_exchange = contract.m_exchange
    return filt


def make_msg_counter(rec_map, unrec_map):
    for classes in list(message.registry.values()):
        for cls in [c for c in classes if True]:
            if not cls.__name__.endswith('Pre') and not cls.__name__.endswith('Post'):
                rec_map[cls] = []
    def counter(msg):
        cls = msg.__class__
        try:
            rec_map[cls].append(msg)
        except (KeyError, ):
            unrec_map.setdefault(cls, []).append(msg)
    return counter


def make_error_catcher(seq):
    def catcher(msg):
        seq.append(msg)
    return catcher


def maybe_verbose(call):
    name = call.__name__
    def inner(connection, options):
        logging.info('Start  %s', name)
        start = time()
        v = call(connection, options)
        finish = time()
        logging.info('Finish %s in %0.3f sec', name, finish-start)
        return v
    inner.__name__ = name
    return inner


def catch_errors(call):
    def inner(connection, options):
        errors = []
        catcher = make_error_catcher(errors)
        connection.register(catcher, 'Error')
        call(connection, options)
        connection.unregister(catcher, 'Error')
        return errors
    inner.__name__ = call.__name__
    return inner


def test_000(connection, options):
    connection.setServerLogLevel(5)
    connection.reqCurrentTime()
    connection.reqAccountUpdates(1, 'DF16165')
    connection.reqManagedAccts()
    connection.requestFA(connection.GROUPS)
    connection.replaceFA(connection.GROUPS, '')
    connection.reqIds(10)


def test_001(connection, options):
    ticker_id = gen_tick_id()
    subscript = ScannerSubscription()
    subscript.numberOfRows(3)
    subscript.locationCode('STK.NYSE')
    connection.reqScannerSubscription(ticker_id, subscript)
    connection.reqScannerParameters()
    short_sleep()
    connection.cancelScannerSubscription(ticker_id)


def test_002(connection, options):
    ticker_id = gen_tick_id()
    contract = make_contract('NVDA')
    connection.reqMktData(ticker_id, contract, generic_tick_keys, False)
    short_sleep()
    connection.cancelMktData(ticker_id)


def test_003(connection, options):
    ticker_id = gen_tick_id()
    contract = make_contract('GOOG')
    connection.reqMktDepth(ticker_id, contract, 10)
    short_sleep()
    connection.cancelMktDepth(ticker_id)


def test_004(connection, options):
    connection.reqAllOpenOrders()
    connection.reqAutoOpenOrders(True)
    connection.reqOpenOrders()
    connection.reqExecutions(0, exec_filter(options.clientid))


def test_005(connection, options):
    connection.reqNewsBulletins(True)
    short_sleep()
    connection.cancelNewsBulletins()


def test_006(connection, options):
    try:
        askprice = [m.price for m in tick_msgs
                    if (getattr(m, 'price', None) is not None) and m.field==2][0]
    except (IndexError, ):
        askprice = 100.0
    order = make_order(askprice)
    if options.demo:
        connection.placeOrder(id=next_order_id(),
                              contract=make_contract('NVDA'),
                              order=order)
    #connection.exerciseOptions()
    contract = make_contract('NVDA')
    connection.reqContractDetails(3, contract)


def test_007(connection, options):
    endtime = strftime('%Y%m%d %H:%M:%S')
    ticker_id = gen_tick_id()
    connection.reqHistoricalData(
            tickerId=ticker_id,
            contract=make_contract('INTC'),
            endDateTime=endtime,
            durationStr='2 D',
            barSizeSetting='30 mins',
            whatToShow='TRADES',
            useRTH=0,
            formatDate=1)
    short_sleep()
    connection.cancelHistoricalData(ticker_id)


def test_008a(connection, options):
    c = Contract()
    c.m_exchange = 'IDEALPRO'
    c.m_symbol = 'MO'
    c.m_localSymbol = 'MO1C'
    c.m_secType = 'BAG'
    c.m_expiry = '200806'
    leg1 = ComboLeg()
    leg1.m_conId = 123
    leg1.m_ratio = 1
    leg1.m_exchange = 'ONE'
    leg1.m_action = 'SELL'
    leg2 = ComboLeg()
    leg2.m_conId = 125
    leg2.m_ratio = 100
    leg2.m_exchange = 'NYSE'
    leg2.m_action = 'BUY'
    c.m_comboLegs = [leg1, leg2]
    connection.reqMktData(1, c, generic_tick_keys, False)


def test_008b(connection, options):
    def cb(*a, **b):
        pass
    connection.register(cb, 'ExecDetails')
    filtr = exec_filter(options.clientid)
    connection.reqExecutions(1, filtr)
    c = Contract()
    c.m_symbol = 'GOOG'
    c.m_secType = 'OPT'
    c.m_exchange = 'SMART'
    c.m_right = 'CALL'
    c.m_strike = 360.0
    c.m_expiry = '200806'
    connection.reqMktData(2, c, '', False)
    long_sleep()


def test_009(connection, options):
    ticker_id = gen_tick_id()
    connection.reqRealTimeBars(ticker_id, make_contract('AAPL'), 5, 'TRADES', 0)
    short_sleep()


def test_010(connection, options):
    connection.reqPositions()
    short_sleep()
    connection.cancelPositions()


def test_011(connection, options):
    reqId = gen_tick_id()
    connection.reqAccountSummary(reqId, 'All', 'AccountType,NetLiquidation')
    short_sleep()
    connection.cancelAccountSummary(reqId)


def test_999(connection, options):
    short_sleep()
    connection.eDisconnect()

def last_wait(connection, options):
    pass


def name_count(value):
    if value.count(':') == 1:
        name, count = value.split(':')
        try:
            count = int(count)
        except (TypeError, ValueError, ):
            count = 0
    else:
        name, count = value, 0
    return name, count


def get_options():
    version = '%prog 0.1'
    parser = OptionParser(version=version)
    add = parser.add_option
    add('-d', '--demo', dest='demo', action='store_true',
        help='Server using demo account, safe for placing orders')
    add('-m', '--messages', dest='printmsgs', action='store_true',
        help='Print message type names and exit')
    add('-s', '--show', dest='showmsgs', metavar='MSG[:MAX]', action='append',
        help=('Print no more than MAX messages of type MSG, may use ALL to '
              'print all messages, may be repeated'), default=[])
    add('-n', '--host', dest='host', default='localhost',
        help='Name or address of remote server (default: %default)')
    add('-p', '--port', dest='port', default=7496, type='int',
        help='Port number for remote connection (default: %default)')
    add('-c', '--client', dest='clientid', metavar='ID', default=0, type='int',
        help='Client id for remote connection (default: %default)')
    add('-v', '--verbose', default=0, action='count',
        help='Verbose output, may be repeated')
    opts, args = parser.parse_args()
    return opts


def main(options):
    basicConfig()
    logging.root.setLevel(verbose_levels.get(options.verbose, ERROR))

    rec_msgs = {}
    unrec_msgs = {}

    handler = make_msg_counter(rec_msgs, unrec_msgs)

    ## make_msg_counter fills in the defaults for the rec_msgs dict; now we can
    ## print those values and exit if the option is given
    if options.printmsgs:
        for name in sorted(k[0].typeName for k in list(rec_msgs.keys())):
            print(name)
        return

    ## if we're still here, we should connect
    con = ibConnection(options.host, options.port, options.clientid)
    con.registerAll(handler)
    con.register(save_order_id, 'NextValidId')
    con.register(save_tick, 'TickSize', 'TickPrice')
    con.connect()
    short_sleep()

    ## and if we've connected, we shoud execute all of the test functions in
    ## the module namespace.
    calls = [v for k, v in list(globals().items()) if k.startswith('test_')]
    for call in sorted(calls, key=lambda f: f.__name__):
        call = maybe_verbose(catch_errors(call))
        errors = call(con, options)
        for err in errors:
            error_msgs[err] = call.__name__

    type_count = len(rec_msgs)
    seen_items = list(rec_msgs.items())
    seen = [(k, v) for k, v in seen_items if v]
    unseen = [(k, v) for k, v in seen_items if not v]

    ## adjust the showmsgs option if given --show=all
    alls = [v for v in options.showmsgs if 'all' in v.lower()]
    if any(alls):
        all, count = name_count(alls[0])
        options.showmsgs = ['%s:%s' % (k.typeName, count) for k in list(rec_msgs.keys())]

    ## ready, set, print!
    for msg_typename in options.showmsgs:
        msg_typename, msg_showmax = name_count(msg_typename)
        formatter = msg_formatters.get(msg_typename, msg_formatters['default'])
        msgs = [v for k, v in seen_items if k.typeName==msg_typename]
        if msgs:
            msgs = msgs[0]
            if not msg_showmax or msg_showmax > len(msgs):
                msg_showmax = len(msgs)
            print('\n%s (%s of %s):' % (msg_typename, msg_showmax, len(msgs), ))
            for msg in msgs[0:msg_showmax]:
                print(formatter(msg))
        else:
            if msg_typename in [k.typeName for k in list(rec_msgs.keys())]:
                print('\n%s (%s):' % (msg_typename, 0, ))
            else:
                print('\nMessage type %s not recognized' % (msg_typename, ))

    ## but wait, there's more!  here we print a summary of seen message
    ## types and associated counts.
    if seen:
        print('\nSeen Message Types (count):')
        for cls, seq in sorted(seen, key=lambda t: t[0].typeName):
            print('    %s (%s)' % (cls.__name__, len(seq), ))
    else:
        print('\nTotal failure; no messages received.')
    ## but wait, there's more!  here we print a summary of unseen message
    ## types and associated counts.
    if unseen:
        print('\nUnseen Message Types (help):')
        for cls, zero in sorted(unseen, key=lambda t: t[0].typeName):
            name = cls.__name__
            help = unseen_hints.get(name, '')
            print('    %s%s' % (name, ' (%s)' % help if help else '', ))
    else:
        print('\nAll Message types received.')
    ## last but not least we print the seen and unseen totals, and their ratio
    print('\nSummary:')
    args = (type_count, len(seen), len(unseen), 100*len(seen)/float(type_count))
    print('   total:%s  seen:%s  unseen:%s  coverage:%2.2f%%' % args)


if __name__ == '__main__':
    try:
        main(get_options())
    except (KeyboardInterrupt, ):
        print('\nKeyboard interrupt.\n')
