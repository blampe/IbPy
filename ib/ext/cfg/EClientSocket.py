#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.ext.cfg.EClientSocket -> config module for EClientSocket.java.

"""
modulePreamble = [
    'from logging import debug',
    '',
    'from ib.ext.AnyWrapper import AnyWrapper',
    'from ib.ext.ComboLeg import ComboLeg',
    'from ib.ext.EClientErrors import EClientErrors',
    'from ib.ext.EReader import EReader',
    'from ib.ext.Util import Util',
    '',
    'from ib.lib.overloading import overloaded',
    'from ib.lib import synchronized, Socket, DataInputStream, DataOutputStream',
    'from ib.lib import Double, Integer',
    '',
    'from socket import SHUT_RDWR',
    'from threading import RLock',
    'mlock = RLock()',
    ]


outputSubs = [
    (r'    m_reader = EReader\(\)', r'    m_reader = None'),
    (r'    m_anyWrapper = AnyWrapper\(\)', r'    m_anyWrapper = None'),
    (r'    m_dos = DataOutputStream\(\)', r'    m_dos = None'),
    (r'EOL = \[0\]', r'EOL = 0'),
    (r'(, "" \+ e)', r', str(e)'),

    (r'print "Server Version:" \+ self\.m_serverVersion',
     r'debug("Server Version:  %s", self.m_serverVersion)',),

    (r'print "TWS Time at connection:" \+ self\.m_TwsTime',
     r'debug("TWS Time at connection:  %s", self.m_TwsTime)',),

    (r'        return strval is None or len\(\(strval\) == 0\)',
     r'        return not bool(strval)'),

    ]


methodPreambleSorter = cmp
