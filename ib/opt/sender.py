#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Sender class to handle outbound requests.
#
# Sender instances defer failed attribute lookup to their
# EClientSocket member objects.
#
##
from functools import wraps

from ib.ext.EClientSocket import EClientSocket
from ib.lib import toTypeName
from ib.opt.message import registry, clientSocketMethods


class Sender(object):
    """ Encapsulates an EClientSocket instance, and proxies attribute
        lookup to it.

    """
    client = None

    def __init__(self, dispatcher):
        """ Initializer.

        @param dispatcher message dispatcher instance
        """
        self.dispatcher = dispatcher
        self.clientMethodNames = [m[0] for m in clientSocketMethods]

    def connect(self, host, port, clientId, handler, clientType=EClientSocket):
        """ Creates a TWS client socket and connects it.

        @param host name of host for connection; default is localhost
        @param port port number for connection; default is 7496
        @param clientId client identifier to send when connected
        @param handler object to receive reader messages
        @keyparam clientType=EClientSocket callable producing socket client
        @return True if connected, False otherwise
        """
        def reconnect():
            self.client = client = clientType(handler)
            client.eConnect(host, port, clientId)
            return client.isConnected()
        self.reconnect = reconnect
        return self.reconnect()

    def disconnect(self):
        """ Disconnects the client.

        @return True if disconnected, False otherwise
        """
        client = self.client
        if client and client.isConnected():
            client.eDisconnect()
            return not client.isConnected()
        return False

    def __getattr__(self, name):
        """ x.__getattr__('name') <==> x.name

        @return named attribute from EClientSocket object
        """
        try:
            value = getattr(self.client, name)
        except (AttributeError, ):
            raise
        if name not in self.clientMethodNames:
            return value
        return value
        preName, postName = name+'Pre', name+'Post'
        preType, postType = registry[preName], registry[postName]
        @wraps(value)
        def wrapperMethod(*args):
            mapping = dict(zip(preType.__slots__, args))
            results = self.dispatcher(preName, mapping)
            if not all(results):
                return # raise exception instead?
            result = value(*args)
            self.dispatcher(postName, mapping)
            return result # or results?
        return wrapperMethod
