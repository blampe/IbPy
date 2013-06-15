#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg -> configuration package and modules for generated code.

This file sets the defaults for source transformation.  The other
modules correspond (1-1) to input java files.  The individual modules
allow for per-file transformation settings.

"""
from java2python.config.default import modulePrologueHandlers

indent = 4


modulePrologueHandlers += [
    '#',
    '# Original file copyright original author(s).',
    '# This file copyright Troy Melhase, troy@gci.net.',
    '#',
    '# WARNING: all changes to this file will be lost.',
    '',
]

outputSubs = [
    (r'if self == p_other:', r'if self is p_other:'),
    (r'if \(self == p_other\):', r'if self is p_other:'),
    (r'(\w+)(\.compareToIgnoreCase\((.*?)\))', r'cmp(\1.lower(), \3.lower())'),
    (r'Integer\.toString', 'str'),
    (r'Double\.toString', 'str'),
    (r'String\.valueOf\(', 'str\('),
    (r'Math\.', ''),
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
