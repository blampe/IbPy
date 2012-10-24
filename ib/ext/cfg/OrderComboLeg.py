#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.OrderComboLeg -> config module for OrderComboLeg.java.

"""
from java2python.config.default import modulePrologueHandlers

modulePrologueHandlers += [
    'from ib.lib import Double',
    'from ib.lib.overloading import overloaded',
    ]
