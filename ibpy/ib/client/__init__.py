#!/usr/bin/env python
""" ib.client -> simple interface for creating IB TWS connections.

"""
from ib.client.writer import ConnectedWriter
from ib.client.threadreader import ThreadingReader


def build(clientId=0, readerType=ThreadingReader):
    """ build(clientId=0, ...) -> new ib connection with threading reader

    """
    return ConnectedWriter(clientId=clientId, readerType=readerType)


try:
    from ib.client.qthreadreader import QThreadReader
except (ImportError, ), exc:
    def build_qt(clientId=0, readerType=None):
        """ build_qt(clientId=0, ...) -> QThread not available.

        """
        raise exc
else:
    def build_qt(clientId=0, readerType=QThreadReader):
        """ build_qt(clientId=0, ...) -> new ib connection with QThread reader

        """
        return build(clientId=clientId, readerType=readerType)
