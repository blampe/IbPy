#!/usr/bin/env python
from ib import lib
from ib.client.writer import CLIENT_VERSION


class Connection(object):
    """ Connection(...) -> useful wrapper of a socket for IB

    This type defines methods for requesting ticker data, account data, etc.

    When called to connect, this type constructs a python socket, connects 
    it to TWS, and if successful, creates and starts a reader object.  The
    reader object is then responsible for slurping data from the connection 
    and doing something with it.
    """
    READER, WRITER, PRE, POST = range(4)

    
    def __init__(self, clientId, reader, writer, socket):
        self.clientId = clientId
        self.reader = reader
        self.writer = writer
        self.socket = reader.socket = writer.socket = socket
        lib.logger.debug('Using socket object %s for %s', socket, self)


    def connect(self, address, clientVersion=CLIENT_VERSION):
        """ connect((host, port)) -> connect to TWS and start reading messages
        
        """
        debug = lib.logger.debug
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
        """ disconnect() -> close the connection by closing the socket

        This causes an exception if the socket is active, but that
        exception gets caught by the stop reader.

        @return None
        """
        lib.logger.debug('Closing socket on object %s', self)
        self.socket.close()
        lib.logger.debug('Socked closed on object %s', self)


    def register(self, messageItem, listener, which=READER, when=POST):
        """ register(...) -> add listner to reader/writer pre/post lists

        @param messageItem message key or message type
        @param listener callable to invoke with generated messages
        @keyparam which may be connection.READER or connection.WRITER
        @keyparam when may be connection.PRE or connection.POST
        @return None
        """
        if which == self.READER:
            for msgid, decoder in self.reader.decoders.items():
                if isinstance(decoder, (messageItem, )) or msgid == messageItem:
                    if when == self.POST:
                        seq = decoder.listeners[1]
                    else:
                        seq = decoder.listeners[0]
                    try:
                        seq.index(listener)
                    except (ValueError, ):
                        seq.append(listener)
        elif which == self.writer:
            pass


    def deregister(self, listener, messageItem, post=True):
        """ deregister(listener) -> remove listener from message receivers

        """
        for msgid, decoder in self.reader.decoders.items():
            if isinstance(decoder, (messageItem, )) or msgid == messageItem:
                if post:
                    seq = decoder.listeners[1]
                else:
                    seq = decoder.listeners[0]
                try:
                    seq.remove(listener)
                except (ValueError, ):
                    pass


    def __getattr__(self, name):
        try:
            return getattr(self.writer, name)
        except (AttributeError, ):
            return getattr(self.reader, name)

