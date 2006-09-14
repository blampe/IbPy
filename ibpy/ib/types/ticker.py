#!/usr/bin/env python
""" Defines the TickType class.

"""


class TickType(object):
    """ TickType(...) -> ticker tick type

    """
    BID_SIZE, BID_PRICE, \
    ASK_PRICE, ASK_SIZE, \
    LAST_PRICE, LAST_SIZE, \
    HIGH, LOW, VOLUME, CLOSE, \
    BID_OPTION, ASK_OPTION, LAST_OPTION = range(0, 13)


    def __getitem__(self, index):
        """ t[i] -> type string at i

        Return strings do not match the IB implementation
        """
        try:
            mapping = dict([(v,k) for k, v in self.__class__.__dict__.items()])
            friendly = mapping[index]            
        except (KeyError, ):
            friendly = 'unknown'
        else:
            friendly = friendly.lower().replace('_', '')
            friendly = friendly.replace('option', 'OptComp')
        return friendly
