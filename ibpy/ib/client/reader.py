#!/usr/bin/env python
""" ib.client.reader -> Interactive Brokers socket reader

This module plus the messages.py module roughly correspond to the IB
TWS Java Client EReader.java source.
"""
from struct import unpack

from ib import lib
from ib.client import message


## incoming message ids.  reader start and stop message ids are local
## to this package.
(
TICK_PRICE, TICK_SIZE, ORDER_STATUS, ERR_MSG, OPEN_ORDER, ACCT_VALUE,
PORTFOLIO_VALUE, ACCT_UPDATE_TIME, NEXT_VALID_ID, CONTRACT_DATA,
EXECUTION_DATA, MARKET_DEPTH, MARKET_DEPTH_L2, NEWS_BULLETINS,
MANAGED_ACCTS, RECEIVE_FA, HISTORICAL_DATA, BOND_CONTRACT_DATA,
SCANNER_PARAMETERS, SCANNER_DATA, TICK_OPTION_COMPUTATION,
) = range(1, 22)

READER_START, READER_STOP = -2, -1

decoderMap = {
    TICK_PRICE : message.TickPrice,
    TICK_SIZE : message.TickSize,
    ORDER_STATUS : message.OrderStatus,
    ERR_MSG : message.Error,
    OPEN_ORDER : message.OpenOrder,
    ACCT_VALUE : message.AccountValue,
    PORTFOLIO_VALUE : message.Portfolio,
    ACCT_UPDATE_TIME : message.AccountTime,
    NEXT_VALID_ID : message.NextId,
    CONTRACT_DATA : message.ContractDetails,
    EXECUTION_DATA : message.Execution,
    MARKET_DEPTH : message.MarketDepth,
    MARKET_DEPTH_L2 : message.MarketDepthLevel2,
    NEWS_BULLETINS : message.NewsBulletin,
    MANAGED_ACCTS : message.ManagedAccounts,
    RECEIVE_FA : message.ReceiveFa,
    HISTORICAL_DATA : message.HistoricalData,
    BOND_CONTRACT_DATA : message.BondContractData,
    SCANNER_PARAMETERS : message.ScannerParameters,    
    SCANNER_DATA : message.ScannerData,
    TICK_OPTION_COMPUTATION : message.TickOptionComputation,

    READER_START : message.ReaderStart,
    READER_STOP : message.ReaderStop,
}


logger = lib.logger()


class Reader(object):
    """ Reader(...) -> TWS socket data reader base class

    This class provides the logic for reading a socket when called to 'run()'.
    Subclasses mix this type in to the appropriate threading library type 
    (e.g., python threading.Thread or Qt QThread)
    """
    def __init__(self, decoders=None):
        object.__init__(self)
        self.active = 0
        self.tokens = []
        self.lastValue = ''
        self.decoders = dict([(id, dcdr()) for id, dcdr in decoderMap.items()])
        ## this enables the ticker price message handler to call our
        ## tick size handlder.
        self.decoders[TICK_PRICE].sizer = self.decoders[TICK_SIZE]


    def run(self):
        """ run() -> read socket data encoded by TWS 

        """
        decoders = self.decoders        
        decoders[READER_START].preDispatch()        
        logger.debug('Begin %s', self)
        ri, rf, rs = self.readInteger, self.readFloat, self.readString
        self.active = 1
        decoders[READER_START].postDispatch()
        
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
                ## reader dispatches it's own messages
                reader.read(ri, rf, rs)

            except (Exception, ), ex:
                decoders[READER_STOP].preDispatch()
                self.active = 0
                msg = 'Reading stopped on Exception %s during message dispatch'
                logger.error(msg, ex)
                decoders[READER_STOP].postDispatch(exception='%s' % (ex, ))


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


class LegacyReader(Reader):
    """ The class with just the original readString implementation.

    Useful reference implementation.
    """
    def readString(self):
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
