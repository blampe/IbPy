#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.Util -> config module for Util.java.

"""
from java2python.config.default import modulePrologueHandlers
from cfg import outputSubs

modulePrologueHandlers += [
    'from ib.lib import Double, Integer',
    ]


outputSubs += [
    (r'cls\.NormalizeString\(lhs\)\.compareTo\(cls\.NormalizeString\(rhs\)\)',
     r'cmp(str(lhs), str(rhs))'),

    (r'cls\.NormalizeString\(lhs\)\.compareToIgnoreCase\(cls\.NormalizeString\(rhs\)\)',
     r'cmp(str(lhs).lower(), str(rhs).lower())'),

    (r'else "" \+ value',
     r'else str(value)'),

    (r'len\(\(strval\) == 0\)', r'(len(strval) == 0)'),

    ]
