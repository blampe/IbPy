#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Sugary sweet layer of icing on top of the TWS API.
#
# Use:
#    {{{
#    from ib.opt import ibConnection, message
#
#    def my_callback(msg):
#        ...
#
#    con = ibConnection()
#    con.register(my_callback, message.TickSize, message.TickPrice)
#    con.connect()
#    con.reqAccountUpdates(...)
#    ...
#    con.unregister(my_callback, message.TickSize)
#    }}}
#
# Enable and disable logging:
#
#    {{{
#    con.enableLogging()
#    ...
#    con.enableLogging(False)
#    }}}
##

from ib.opt.logger import logger
from ib.opt.receiver import Receiver
from ib.opt.sender import Sender


class Connection(object):
    """ Encapsulates a connection to TWS.

    """
    def __init__(self, host, port, clientId):
        """ Constructor.

        @param host name of host for connection; default is localhost
        @param port port number for connection; default is 7496
        @param clientId client identifier to send when connected
        """
        self.host = host
        self.port = port
        self.clientId = clientId
        self.receiver = Receiver()
        self.sender = Sender()

    def __getattr__(self, name):
        """ x.__getattr__('name') <==> x.name

        @return named attribute from instance receiver or sender
        """
        try:
            return getattr(self.receiver, name)
        except (AttributeError, ):
            try:
                return getattr(self.sender, name)
            except (AttributeError, ):
                pass
        raise AttributeError(name)

    def connect(self):
        """ Establish a connection to TWS with instance attributes.

        @return None
        """
        self.sender.connect(self.host, self.port, self.clientId, self.receiver)

    def enableLogging(self, enable=True):
        """ Enable or disable logging of all messages.

        @param enable if True (default), enables logging; otherwise disables
        @return None
        """
        if enable:
            self.logger = logger()
            self.receiver.registerAll(self.logMessage)
        else:
            self.receiver.unregisterAll(self.logMessage)

    def logMessage(self, message):
        """ Format and send a message values to the logger.

        @param message instance of Message
        @return None
        """
        line = str.join(', ', ['%s=%s' % item for item in message.items()])
        self.logger.debug('%s(%s)', message.__class__.__name__, line)


    @classmethod
    def create(cls, host='localhost', port=7496, clientId=0):
        """ Creates and returns Connection class (or subclass) instance.

        @param host name of host for connection; default is localhost
        @param port port number for connection; default is 7496
        @param clientId client identifier to send when connected
        @return Connection (or subclass) instance
        """
        return cls(host=host, port=port, clientId=clientId)

##
# This is the preferred client interface to this module.
# Alternatively, the Connection type can be sub-classed an its create
# classmethod reused
ibConnection = Connection.create
