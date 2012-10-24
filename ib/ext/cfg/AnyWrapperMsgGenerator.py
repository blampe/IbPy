#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.AnyWrapperMsgGenerator -> config module for AnyWrapperMsgGenerator.java.

"""
from cfg import outputSubs
from java2python.config.default import modulePrologueHandlers
modulePrologueHandlers += [
    'from ib.lib import classmethod_ as classmethod',
    'from ib.lib.overloading import overloaded',
    ]


outputSubs += [
    (r'return "Error - " \+ ex',
     r'return "Error - " + ex.message'),
    ]
