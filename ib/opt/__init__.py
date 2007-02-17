#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.opt -> a sugary sweet layer of icing on top of the TWS API.

Use:

    from ib import ib_connection

    c = ib_connection()

    c.register(my_callback, c.TICK_TYPE, c.TICK_SIZE)
    c.unregister(my_callback, c.TICK_TYPE)

    c.connect()


"""

from ib.aux.overloading import overloaded
from ib.ext.EClientSocket import EClientSocket
from ib.ext.EReader import EReader
from ib.ext.EWrapper import EWrapper


def ib_connection(host='localhost', port=7496, clientId=0):
    return Connection()


class Connection(object):

    def __init__(self):
        self.sender = Sender()
        self.receiver = Receiver()

    def connect(self, host, port, clientId):
        self.sender.connect(host, port, clientId)

    def register(self, listener, *messages):
        """

        @param messages integer message codes
        """

    def __getattr__(self, name):
        try:
            return getattr(self.receiver, name)
        except (AttributeError, ):
            try:
                return getattr(self.sender, name)
            except (AttributeError, ):
                pass
        raise AttributeError(name)


class Sender(object):
    """

    objects call listeners pre/post reqScannerParameters,
    reqAccountUpdates, etc.

    """
    def __init__(self, ):
        self.client = None

    def connect(self, host, port, clientId):
        self.client = EClientSocket(self)
        self.client.eConnect(host, port, clientId)

    @overloaded
    def error(self, e):
        raise NotImplementedError()

    @error.register(object, str)
    def error_0(self, strval):
        raise NotImplementedError()

    @error.register(object, int, int, str)
    def error_1(self, id, errorCode, errorMsg):
        raise NotImplementedError()

    def connectionClosed(self):
        raise NotImplementedError()

    def __getattr__(self, name):
        try:
            return getattr(self.client, name)
        except (AttributeError, ):
            return getattr(EClientSocket, name)



class Receiver(object):
    """

    objects generate messages and call listeners after socket values
    have been read

    """
    def __init__(self):
        self.thread = None
        self.wrapper_names = [n for n in dir(EWrapper)
                                  if not n.startswith('_') and
                                      isinstance(getattr(EWrapper, n), type(self.__init__))]

    def __getattr__(self, name):
        if name == name.upper():
            return getattr(EReader, name)
        if name in self.wrapper_names:
            return self.handle
        raise AttributeError(name)


    def handle(self, *args, **kwds):
        pass


