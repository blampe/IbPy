#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.Contract -> config module for Contract.java.

"""
from java2python.config.default import modulePrologueHandlers
from cfg import outputSubs

modulePrologueHandlers += [
    'from ib.lib.overloading import overloaded',
    'from ib.lib import Cloneable',
    'from ib.ext.Util import Util',
    ]


outputSubs += [
    (r'super\.clone\(\)', r'Cloneable.clone(self)'),
    (r'retval\.m_comboLegs\.clone\(\)', r'self.m_comboLegs[:]'),
    (r'    m_comboLegs = \[\]', r'    m_comboLegs = None'),
    (r'    m_underComp = UnderComp\(\)', r'    m_underComp = None'),
    (r'    def __init__\(self\)\:',
     r'    def __init__(self):\n        self.comboLegs = []'),
    ]
