#!/usr/bin/env python
# -*- coding: utf-8 -*-

headings = {
    'Contract.java' : [
    'from helpers import *',
    ],
    
    'ContractDetails.java' : [
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
    (r"(\.self\.)", "."),
###    (r"(.*)(\.size\(\))", r"\1len(\2)"),
    
    
    ]


## l_thisSecType.equals("BOND"):
## l_thisSecType == "BOND"


