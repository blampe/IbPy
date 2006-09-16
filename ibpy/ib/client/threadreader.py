#!/usr/bin/env python
""" ib.client.threadreader -> Threaded IB TWS socket reader

"""
from threading import Thread
from ib.client.reader import Reader


class ThreadingReader(Thread, Reader):
    """ ThreadingReader(...) -> basic thread reader

    """
    def __init__(self, readers, socket):
        Thread.__init__(self)
        Reader.__init__(self, readers, socket)
        self.setDaemon(True)


    def run(self):
        Reader.run(self)
