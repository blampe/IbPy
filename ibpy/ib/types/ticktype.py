#!/usr/bin/env python
""" Defines the TickType class.

"""


class TickType(object):
    """ TickType() -> tick type

    """
    (
    BID_SIZE, BID, ASK, ASK_SIZE, LAST, LAST_SIZE,
    HIGH, LOW, VOLUME, CLOSE, BID_OPTION, ASK_OPTION, LAST_OPTION,
    ) = range(0, 13)

    keys = {
        BID_SIZE : 'bidSize',
        BID : 'bidPrice',
        ASK : 'askPrice',
        ASK_SIZE : 'askSize',
        LAST : 'lastPrice',
        LAST_SIZE : 'lastSize',
        HIGH : 'high',
        LOW : 'low',
        VOLUME : 'volume',
        CLOSE : 'close',
        BID_OPTION : 'bidOptComp',
        ASK_OPTION : 'askOptComp',
        LAST_OPTION : 'lastOptComp',
        None : 'unknown',
    }


    def __getitem__(self, index):
        """ tick[i] -> string at i

        """
        try:
            return self.keys[index]
        except (KeyError, ):
            return self.keys[None]
        
