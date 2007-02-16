modulePreamble = [
    'from ib.aux.overloading import overloaded',
    'from ib.ext.Contract import Contract',
    ]

outputSubs = [
    (r'    m_summary = Contract\(\)', r'    m_summary = None'),
    ]

