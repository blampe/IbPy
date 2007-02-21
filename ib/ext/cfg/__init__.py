#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg -> configuration package and modules for generated code.

This file sets the defaults for source transformation.  The other
modules correspond (1-1) to input java files.  The individual modules
allow for per-file transformation settings.

"""
indent = 4


modulePreamble = [
    '##',
    '#',
    lambda module:'# Source file: "%s"' % module.infile,
    lambda module:'# Target file: "%s"' % module.outfile,
    '#',
    '# Original file copyright original author(s).',
    '# This file copyright Troy Melhase, troy@gci.net.',
    '#',
    '##',
    '',
]


modifierDecoratorMap = {
    'synchronized':'@synchronized(mlock)'
}


outputSubs = [
    (r'if self == p_other:', r'if self is p_other:'),
    (r'if \(self == p_other\):', r'if self is p_other:'),
    (r'(\w+)(\.compareToIgnoreCase\((.*?)\))', r'cmp(\1.lower(), \3.lower())'),
    ]


renameAnyMap = {
    'exec':'exec_',
    }


variableNameMapping = {
    'exec':'exec_',
    }


renameMethodMap = {
    'equals':'__eq__',
    'is':'is_',
}
