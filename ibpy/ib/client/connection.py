#!/usr/bin/env python
from socket import AF_INET, SOCK_STREAM
from socket import socket as sockettype

from ib import lib
from ib.client.writer import CLIENT_VERSION


logger = lib.logger()


class Connection(object):
    """ Connection(...) -> useful wrapper of a socket for IB

    This type defines methods for requesting ticker data, account data, etc.

    When called to connect, this type constructs a python socket, connects 
    it to TWS, and if successful, creates and starts a reader object.  The
    reader object is then responsible for slurping data from the connection 
    and doing something with it.
    """
    def __init__(self, clientId, reader, writer, socket=None):
        self.clientId = clientId
        self.reader = reader
        self.writer = writer
        
        if socket is None:
            socket = sockettype(AF_INET, SOCK_STREAM)
            logger.debug('Created socket object %s for %s', socket, self)
        self.socket = reader.socket = writer.socket = socket


    def connect(self, address, clientVersion=CLIENT_VERSION):
        """ connect((host, port)) -> connect to TWS and start reading messages
        
        """
        debug = logger.debug
        reader = self.reader
        writer = self.writer
        
        self.socket.connect(address)
        debug('Connected object %s to address %s', self, address)

        writer.send(clientVersion)
        debug('Sent client version %s', clientVersion)

        serverVersion = reader.serverVersion = writer.serverVersion = \
                        reader.readInteger()
        debug('Read server version %s', serverVersion)

        if serverVersion >= 20:
            twsTime = reader.readString()
            debug('Received server TwsTime: %s', twsTime)

        if serverVersion >= 3:
            debug('Sending client id %s for object %s', self.clientId, self)
            writer.send(self.clientId)

        debug('Starting reader for object %s', self)
        reader.start()


    def disconnect(self):
        """ disconnect() -> close the socket.

        This causes an exception if the socket is active, but that
        exception gets caught by the stop reader.
        """
        logger.debug('Closing socket on object %s', self)
        self.socket.close()
        logger.debug('Socked closed on object %s', self)


    def __getattr__(self, name):
        try:
            return getattr(self.writer, name)
        except (AttributeError, ):
            return getattr(self.reader, name)
        
