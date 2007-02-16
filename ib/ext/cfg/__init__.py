indent = 4

typeTypeMap = {
    }


modulePreamble = [
    '##',
    lambda module:'## Source file: "%s"' % module.infile,
    lambda module:'## Target file: "%s"' % module.outfile,
    '##',
    '## Original file copyright original author(s).',
    '## This file copyright Troy Melhase <troy@gci.net>.',
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



moduleEpilogue = [
    ]


renameAnyMap = {
    'exec':'exec_',
    }

variableNameMapping = {
    'exec':'exec_',
    }


renameMethodMap = {
    'equals':'__eq__',
##    'clone':'__copy__',
    'is':'is_',
}
