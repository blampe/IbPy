modulePreamble = [
    'from ib.aux import Thread, Boolean',
    'from ib.aux import DataInputStream',
    'from ib.aux.overloading import overloaded',
    '',
    'from ib.ext.Contract import Contract',
    'from ib.ext.ContractDetails import ContractDetails',
    'from ib.ext.Order import Order',

    ]

outputSubs = [
    (r'    m_parent = object\(\)', '    m_parent = None'),
    (r'    m_dis = DataInputStream\(\)', '    m_dis = None'),
    ]



typeTypeMap = {
    'EClientSocket':'object'
    }
