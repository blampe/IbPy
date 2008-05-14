#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Connection class to encapsulate a connection to IB TWS.
#
# Connection instances defer failed attribute lookup to their receiver
# and sender member objects.  This makes it easy to access the
# receiver to register functions:
#
# >>> con = ibConnection()
# >>> con.register(my_callable)
#
# And it makes it easy to access the sender functions:
#
# >>> con.reqScannerParameters()
# >>> con.placeOrder(...)
#
##
from ib.lib.logger import logger
from ib.opt.receiver import Receiver
from ib.opt.sender import Sender


class Connection(object):
    """ Encapsulates a connection to TWS.

    """
    def __init__(self, host, port, clientId, receiver, sender):
        """ Constructor.

        @param host name of host for connection; default is localhost
        @param port port number for connection; default is 7496
        @param clientId client identifier to send when connected
        """
        self.host = host
        self.port = port
        self.clientId = clientId
        self.receiver = receiver
        self.sender = sender

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

        @return True if connected, otherwise raises an exception
        """
        return self.sender.connect(self.host, self.port, self.clientId,
                                   self.receiver)

    def disconnect(self):
        """ Disconnect from TWS

        @return True if disconnected, False otherwise
        """
        return self.sender.disconnect()

    def enableLogging(self, enable=True):
        """ Enable or disable logging of all messages.

        @param enable if True (default), enables logging; otherwise disables
        @return True if enabled, False otherwise
        """
        if enable:
            self.logger = logger()
            self.receiver.registerAll(self.logMessage)
        else:
            self.receiver.unregisterAll(self.logMessage)
        return enable

    def logMessage(self, message):
        """ Format and send a message values to the logger.

        @param message instance of Message
        @return None
        """
        line = str.join(', ', ['%s=%s' % item for item in message.items()])
        self.logger.debug('%s(%s)', message.typeName, line)

    @classmethod
    def create(cls, host='localhost', port=7496, clientId=0, receiver=None,
               sender=None):
        """ Creates and returns Connection class (or subclass) instance.

        @param host name of host for connection; default is localhost
        @param port port number for connection; default is 7496
        @param clientId client identifier to send when connected
        @return Connection (or subclass) instance
        """
        receiver = Receiver() if receiver is None else receiver
        sender = Sender() if sender is None else sender
        return cls(host, port, clientId, receiver, sender)
