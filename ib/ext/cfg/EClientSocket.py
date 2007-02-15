modulePreamble = [
    'from ib.ext.AnyWrapper import AnyWrapper',
    'from ib.ext.EClientErrors import EClientErrors',
    'from ib.ext.EReader import EReader',
    '',
    'from ib.aux.overloading import overloaded',
    'from ib.aux import synchronized, Socket, DataOutputStream',
    '',
    'from threading import Lock',
    '',
    'mlock = Lock()',
    ]


outputSubs = [
    (r'    m_reader = EReader\(\)', r'    m_reader = None'),
    ]

def methodPreambleSorter(a, b):
    return cmp(a, b)
