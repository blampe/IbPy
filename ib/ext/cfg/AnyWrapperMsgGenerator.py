#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.AnyWrapperMsgGenerator -> config module for AnyWrapperMsgGenerator.java.

"""
modulePreamble = [
    'from ib.lib import classmethod_ as classmethod',
    'from ib.lib.overloading import overloaded',
    ]


outputSubs = [
    (r'return "Error - " \+ ex',
     r'return "Error - " + ex.message'),
    ]
