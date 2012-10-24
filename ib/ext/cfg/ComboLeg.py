#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.ComboLeg -> config module for ComboLeg.java.

"""
from java2python.config.default import modulePrologueHandlers
from cfg import outputSubs

modulePrologueHandlers += [
    'from ib.lib.overloading import overloaded',
    'from ib.ext.Util import Util',
    ]


outputSubs += [
    (r'(\s+)(super\(ComboLeg, self\).*)', r'\1pass # \2'),
    ]
