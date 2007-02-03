#!/usr/bin/env python
""" Defines the Contract class.

"""
from ib.lib import getattrs, setattrs


class Contract(object):
    """ Contract(...) -> stock or option contract 

    """
    def __init__(self,
                 symbol='',
                 secType='',
                 expiry='',
                 strike=0.0,
                 right='',
                 multiplier='',
                 exchange='',
                 
                 currency='', 
                 localSymbol='',
                 comboLegs=None,
                 primaryExch='',
                 includeExpired=0,

                 ## bond values
                 cusip='',
                 ratings='',
                 descAppend='',
                 bondType='',
                 couponType='',
                 callable=0,
                 putable=0,
                 coupon=0.0,
                 convertible=0,
                 maturity='',
                 issueDate='',
                 nextOptionDate='',
                 nextOptionType='',
                 nextOptionPartial=0,
                 notes=''):
        if comboLegs is None:
            comboLegs = []
        setattrs(self, locals())


    def __str__(self):
        return 'Contract(%s %s %s %s %s %s %s)' % \
               (self.symbol, self.secType, self.expiry, self.strike,
                self.right, self.exchange, self.localSymbol)


    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if len(self.comboLegs) != len(other.comboLegs):
            return False
        if self.secType.lower() != other.secType.lower():
            return False

        syms = ('symbol', 'exchange', 'primaryExch', 'currency')
        if getattrs(self, syms) != getattrs(other, syms):
            return False

        if self.secType == 'BOND':
            syms = ('putable', 'callable', 'convertible', 'coupon',
                    'cuspi', 'ratings', 'descAppend', 'bondType',
                    'couponType', 'maturity', 'issueDate')
            iseq = getattrs(self, syms) == getattrs(other, syms)
        else:
            syms = ('expiry', 'right', 'multiplier', 'localSymbol')
            iseq = getattrs(self, syms) == getattrs(other, syms)

        if iseq and self.comboLegs:
            for thisleg, otherleg in zip(self.comboLegs, other.comboLegs):
                if thisleg != otherleg:
                    iseq = False
        return iseq
