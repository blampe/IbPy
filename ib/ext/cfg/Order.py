#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.Order -> config module for Order.java.

"""
from java2python.config.default import modulePrologueHandlers
modulePrologueHandlers += [
    'from ib.lib import Double, Integer',
    'from ib.ext.Util import Util'
    ]
