#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.Contract -> config module for Contract.java.

"""
modulePreamble = [
    'from ib.lib.overloading import overloaded',
    'from ib.lib import Cloneable',
    'from ib.ext.Util import Util',
    ]


outputSubs = [
    (r'super\.clone\(\)', r'Cloneable.clone(self)'),
    (r'retval\.m_comboLegs\.clone\(\)', r'self.m_comboLegs[:]'),
    ]
