#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.ScannerSubscription -> config module for ScannerSubscription.java.

"""
from java2python.config.default import modulePrologueHandlers

modulePrologueHandlers += [
    'from ib.lib import Double, Integer',
    'from ib.lib.overloading import overloaded',
    ]


fixPropMethods = False
