#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.AnyWrapperMsgGenerator -> config module for AnyWrapperMsgGenerator.java.

"""
modulePreamble = [
    'from ib.lib import cmattr',
    'from ib.lib.overloading import overloaded',
    ]


outputSubs = [
    (r'(\s+)@classmethod\n(\s+)@(.+)',
     r'\1@cmattr\n\2@\3'),

    (r'return "Error - " \+ ex',
     r'return "Error - " + ex.message'),

    (r'Integer\.toString',
     'str'),
    
    ]
