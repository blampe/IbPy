#!/usr/bin/env python
""" Defines the Contract class.

"""
from ib.lib import setattr_mapping, getattrs


class Contract(object):
    """ Contract(...) -> stock or option contract 

    """
    def __init__(self,
                 symbol='',
                 sec_type='',
                 expiry='',
                 strike=0.0,
                 right='',
                 multiplier='',
                 exchange='',
                 currency='', 
                 local_symbol='',
                 combo_legs=None,
                 primary_exchange='',
                 cusip='',
                 ratings='',
                 desc_append='',
                 bond_type='',
                 coupon_type='',
                 callable=False,
                 putable=False,
                 coupon=0.0,
                 convertible=False,
                 maturity='',
                 issue_date=''):
        if combo_legs is None:
            combo_legs = []
        setattr_mapping(self, locals())


    def __str__(self):
        return 'Contract(%s %s %s %s %s %s %s)' % \
               (self.symbol, self.sec_type, self.expiry, self.strike,
                self.right, self.exchange, self.local_symbol)


    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if len(self.combo_legs) != len(other.combo_legs):
            return False
        if self.sec_type.lower() != other.sec_type.lower():
            return False

        syms = ('symbol', 'exchange', 'primary_exchange', 'currency')
        if getattrs(self, syms) != getattrs(other, syms):
            return False

        if self.sec_type == 'BOND':
            syms = ('putable', 'callable', 'convertible', 'coupon',
                    'cuspi', 'ratings', 'desc_append', 'bond_type',
                    'coupon_type', 'maturity', 'issue_date')
            iseq = getattrs(self, syms) == getattrs(other, syms)
        else:
            syms = ('expiry', 'right', 'multiplier', 'local_symbol')
            iseq = getattrs(self, syms) == getattrs(other, syms)

        if iseq and self.combo_legs:
            for thisleg, otherleg in zip(self.combo_legs, other.combo_legs):
                if thisleg != otherleg:
                    iseq = False
        return iseq
