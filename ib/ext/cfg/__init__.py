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
    lambda m:'# Translated source for %s.' % m.outfile[:-3],
    '##',
    '',
    lambda m:'# Source file: %s' % m.infile,
    lambda m:'# Target file: %s' % m.outfile,
    '#',
    '# Original file copyright original author(s).',
    '# This file copyright Troy Melhase, troy@gci.net.',
    '#',
    '# WARNING: all changes to this file will be lost.',
    '',
]


modifierDecoratorMap = {
    'synchronized':'@synchronized(mlock)'
}


outputSubs = [
    (r'if self == p_other:', r'if self is p_other:'),
    (r'if \(self == p_other\):', r'if self is p_other:'),
    (r'(\w+)(\.compareToIgnoreCase\((.*?)\))', r'cmp(\1.lower(), \3.lower())'),
    (r'Integer\.toString', 'str'),
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
