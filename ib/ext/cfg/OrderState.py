#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.OrderState -> config module for OrderState.java.

"""
modulePreamble = [
    'from ib.lib.overloading import overloaded',
    'from ib.ext.Util import Util',
    ]

outputSubs = [
    (r'(\s+)(super\(OrderState, self\).*)', r'\1pass # \2'),
    ]
