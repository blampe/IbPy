#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.ComboLeg -> config module for ComboLeg.java.

"""
modulePreamble = [
    'from ib.lib.overloading import overloaded',
    'from ib.ext.Util import Util',
    ]


outputSubs = [
    (r'(\s+)(super\(ComboLeg, self\).*)', r'\1pass # \2'),
    ]
