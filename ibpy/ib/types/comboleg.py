#!/usr/bin/env python
""" Defines the ComboLeg class.

"""
from ib.lib import setattr_mapping, getattrs


class ComboLeg(object):
    """ ComboLeg(...) -> combo leg
        
    """
    SAME, OPEN, CLOSE, UNKNOWN = range(0, 4)


    def __init__(self,
                 conId=0,
                 ratio=0,
                 action='',
                 exchange='',
                 openClose=0):
        setattr_mapping(self, locals())


    def __eq__(self, other):
        if self is other:
            return True
        if not other:
            return False
        syms = ('action', 'exchange', 'conId', 'ratio', 'openClose')
        return getattrs(self, syms) == getattrs(other, syms)
