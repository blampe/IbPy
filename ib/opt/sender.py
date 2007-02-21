#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Sender class to handle outbound requests.
##

from ib.aux.overloading import overloaded
from ib.ext.EClientSocket import EClientSocket


class Sender(object):
    """

    objects call listeners pre/post reqScannerParameters,
    reqAccountUpdates, etc.

    """
    def __init__(self, ):
        self.client = None

    def connect(self, host, port, clientId, handler):
        self.client = EClientSocket(handler)
        self.client.eConnect(host, port, clientId)

    def __getattr__(self, name):
        return getattr(self.client, name)
