#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.AnyWrapper -> config module for AnyWrapper.java.

"""
from java2python.config.default import modulePrologueHandlers
modulePrologueHandlers += [
    'from ib.lib.overloading import overloaded',
    ]
