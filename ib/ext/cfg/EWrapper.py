#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.EWrapper -> config module for EWrapper.java.

"""
from java2python.config.default import modulePrologueHandlers
modulePrologueHandlers += [
    'from ib.ext.AnyWrapper import AnyWrapper',
    ]
