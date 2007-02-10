#!/usr/bin/env python
# -*- coding: utf-8 -*-


headings = {
    'Contract.java' : [
    'from helpers import *',
    ],
    
    'ContractDetails.java' : [
    'from Contract import Contract',
    'from socket import socket',
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



