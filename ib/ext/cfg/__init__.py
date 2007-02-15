indent = 4

typeTypeMap = {
    }


modulePreable = [
    '##',
    lambda module:'## Source file: "%s"' % module.infile,
    lambda module:'## Target file: "%s"' % module.outfile,
    '##',
    '## Original file copyright original author(s).',
    '## This file copyright Troy Melhase <troy@gci.net>.',
    '##',
    '',
    'from helpers import *',
    'from overloading import overloaded',
    'from Contract import Contract',
]


modifierDecoratorMap = {
    'synchronized':'@synchronized(mlock)'
}


outputSubs = [
    (r'if self == p_other:', r'if self is p_other:'),
    ]



moduleEpilogue = [
    ]


renameAnyMap = {
    'exec':'exec_',
    }

variableNameMapping = {
    'exec':'exec_',
    }
