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

    'ExecutionFilter.java': [
    'from overloading import overloaded',
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
    (r'(.*?)\.equals\((.*?)\)', r'\1 == \2'),
    (r'(.*?)\.equalsIgnoreCase\((.*?)\)', r'\1.lower() == \2.lower()'),
    (r'if self == p_other:', r'if self is p_other:'),
    (r'([\w.]+)\.size\(\)', r'len(\1)'),
    (r'(\w+)\.get\((.*?)\)', r'\1[\2]'),
    ]
