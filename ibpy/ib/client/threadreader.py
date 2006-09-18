#!/usr/bin/env python
""" ib.client.threadreader -> Threaded IB TWS socket reader

"""
from threading import Thread
from ib.client.reader import Reader


class ThreadingReader(Thread, Reader):
    """ ThreadingReader(...) -> basic thread reader

    """
    def __init__(self, decoders=None):
        Thread.__init__(self)
        Reader.__init__(self, decoders)
        self.setDaemon(True)


    def run(self):
        Reader.run(self)
