#!/usr/bin/env python
""" ib.client.reader -> Interactive Brokers socket reader


"""
from struct import unpack

from ib import lib 
from ib.client.writer import READER_START, READER_STOP


## local logger
logger = lib.logger()


class Reader(object):
    """ Reader(...) -> TWS socket data reader base class

    This class provides the logic for reading a socket when called to 'run()'.
    Subclasses mix this type in to the appropriate threading library type 
    (e.g., python threading.Thread or Qt QThread)
    """
    def __init__(self, decoders, socket):
        object.__init__(self)
        self.active = 0
        self.decoders = decoders
        self.socket = socket
        logger.debug('Created %s with fd %s', self, socket.fileno())
        self.tokens = []
        self.lastValue = ''


    def run(self):
        """ run() -> read socket data encoded by TWS 

        """
        logger.debug('Begin %s', self)
        ri, rf, rs = self.readInteger, self.readFloat, self.readString
        decoders = self.decoders
        decoders[READER_START].dispatch()
        self.active = 1

        while self.active:
            try:
                msgId = ri()
                if msgId == -1:
                    break
                reader = decoders[msgId]

                if str(reader) == 'Error':
                    log = logger.warning
                else:
                    log = logger.info

                log(reader)
                reader.read(ri, rf, rs)

            except (Exception, ), ex:
                self.active = 0
                msg = 'Reading stopped on Exception %s during message dispatch'
                logger.error(msg, ex)
                decoders[READER_STOP].dispatch(exception='%s' % (ex, ))


    def readInteger(self):
        """ readInteger() -> read an integer from the socket

        """
        value = self.readString()
        try:
            return int(value)
        except (ValueError, ):
            return 0


    def readFloat(self):
        """ readFloat() -> read and unpack a float from the socket

        """
        value = self.readString()
        try:
            return float(value)
        except (ValueError, ):
            return 0.0


    def readString(self):
        """ readString() -> read and unpack a string from the socket

        """
        bufSize = 2000
        tokens = self.tokens

        while not len(tokens):
            data = self.socket.recv(bufSize)
            fields = data.split('\x00')
            fields[0] = self.lastValue + fields[0]
            self.lastValue = fields.pop(-1)
            tokens.extend(fields)            
            if tokens:
                break
        value = tokens.pop(0)
        return value



    def __readString(self):
        """ legacy readString implementation

        """
        buf_size = 1
        read_bites = []
        read_func = self.socket.recv

        while True:
            socket_read = read_func(buf_size)
            bite = unpack('!s', socket_read)[0]
            if not ord(bite):
                break
            read_bites.append(socket_read)

        read = ''.join(read_bites)
        logger.debug('Socket read bytes %s', read_bites)
        return read


