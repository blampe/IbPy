#!/usr/bin/env python
""" ib.client -> simple interface for creating IB TWS connections.

"""
from ib.client.writer import ConnectedWriter
from ib.client.threadreader import ThreadingReader


def build(clientId=0, readerType=ThreadingReader):
    """ build(clientId=0, ...) -> creates a new ib socket connection

    """
    return ConnectedWriter(clientId=clientId, readerType=readerType)


try:
    from ib.client.qthreadreader import QThreadReader
except (ImportError, ), exc:
    def build_qt(clientId=0, readerType=None):
        raise exc
else:
    def build_qt(clientId=0, readerType=QThreadReader):
        return build(clientId=clientId, readerType=readerType)
