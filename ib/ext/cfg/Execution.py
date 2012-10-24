#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.Execution -> config module for Execution.java.

"""
from java2python.config.default import modulePrologueHandlers
modulePrologueHandlers += [
    'from ib.lib.overloading import overloaded',
    ]
