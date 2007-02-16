modulePreamble = [
    'from ib.ext.AnyWrapper import AnyWrapper',
    'from ib.ext.EClientErrors import EClientErrors',
    'from ib.ext.EReader import EReader',
    '',
    'from ib.aux.overloading import overloaded',
    'from ib.aux import synchronized, Socket, DataInputStream, DataOutputStream',
    'from ib.aux import Double, Integer',
    '',
    'from threading import Lock',
    '',
    'mlock = Lock()',
    ]


outputSubs = [
    (r'    m_reader = EReader\(\)', r'    m_reader = None'),
    (r'    m_anyWrapper = AnyWrapper\(\)', r'    m_anyWrapper = None'),
    (r'    m_socket = Socket\(\)', r'    m_socket = None'),
    (r'    m_dos = DataOutputStream\(\)', r'    m_dos = None'),
    (r'(, "" \+ e)', r', str(e)'),
    ]

def methodPreambleSorter(a, b):
    return cmp(a, b)
