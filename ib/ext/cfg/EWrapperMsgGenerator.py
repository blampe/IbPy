#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.EWrapperMsgGenerator -> config module for EWrapperMsgGenerator.java.

"""
from java2python.config.default import modulePrologueHandlers
modulePrologueHandlers += [
    'from ib.ext.AnyWrapperMsgGenerator import AnyWrapperMsgGenerator',
    'from ib.ext.EClientSocket import EClientSocket',
    'from ib.ext.MarketDataType import MarketDataType',
    'from ib.ext.TickType import TickType',
    'from ib.ext.Util import Util',
    '',
    'from ib.lib import Double',
    ]
