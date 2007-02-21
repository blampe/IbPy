#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Sender class to handle outbound requests.
##

from ib.aux.overloading import overloaded
from ib.ext.EClientSocket import EClientSocket


class Sender(object):
    """ Encapsulates an EClientSocket instance, and proxies attribute
        lookup to it.

    """
    def __init__(self):
        """ Constructor.

        """
        self.client = None

    def connect(self, host, port, clientId, handler):
        """ Creates an EClientSocket and connects it.


        @param host name of host for connection; default is localhost
        @param port port number for connection; default is 7496
        @param clientId client identifier to send when connected
        @param handler object to receive reader messages
        @return None
        """
        self.client = EClientSocket(handler)
        self.client.eConnect(host, port, clientId)

    def __getattr__(self, name):
        """ x.__getattr__('name') <==> x.name

        @return named attribute from instance client object
        """
        return getattr(self.client, name)
