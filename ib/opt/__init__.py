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
from ib.opt.receiver import Receiver
from ib.opt.sender import Sender


def ib_connection(host='localhost', port=7496, clientId=0):
    return Connection(host=host, port=port, clientId=clientId)


class Connection(object):

    def __init__(self, host, port, clientId):
        self.host = host
        self.port = port
        self.clientId = clientId
        self.receiver = Receiver()
        self.sender = Sender()

    def connect(self):
        self.sender.connect(self.host, self.port, self.clientId, self.receiver)

    def __getattr__(self, name):
        try:
            return getattr(self.receiver, name)
        except (AttributeError, ):
            try:
                return getattr(self.sender, name)
            except (AttributeError, ):
                raise AttributeError(name)

