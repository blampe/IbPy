#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.ContractDetails -> config module for ContratDetails.java.

"""
modulePreamble = [
    'from ib.lib.overloading import overloaded',
    'from ib.ext.Contract import Contract',
    ]


outputSubs = [
    (r'    m_summary = Contract\(\)', r'    m_summary = None'),
    ]
