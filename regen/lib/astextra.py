#!/usr/bin/env python
# -*- coding: utf-8 -*-

headings = {
    'Contract.java' : [
    'from helpers import *',
    ],
    
    'ContractDetails.java' : [
    'from overloading import overloaded',
    'from Contract import Contract',
    ],

    'ScannerSubscription.java' : [
    'from helpers import *',
    ],


}
    

features = {
    'ContractDetails.java' : 'rename strip frobinate',
}


defaults = {
    'writemods':False
}



globalSubs = [
    (r'(\.self\.)', '.'),
    (r'String\.valueOf\((.*?)\)', r'str(\1)'),
    (r'System\.out\.println\((.*?)\)', r'print \1'),
    ]

## l_thisSecType.equals("BOND"):
## l_thisSecType == "BOND"

