#!/usr/bin/env python
""" ib.client -> simple interface for creating IB TWS connections.

"""
from socket import AF_INET, SOCK_STREAM
from socket import socket as sockettype

from ib.client.connection import Connection
from ib.client.writer import DefaultWriter
from ib.client.threadreader import ThreadingReader


def build(clientId=0, reader=None, writer=None, socket=None):
    """ build(clientId=0, ...) -> new ib connection with threading reader

    """
    if reader is None:
        reader = ThreadingReader()
    if writer is None:
        writer = DefaultWriter()
    if socket is None:
        socket = sockettype(AF_INET, SOCK_STREAM)
    return Connection(clientId=clientId, reader=reader, writer=writer,
                      socket=socket)


try:
    from ib.client.qthreadreader import QThreadReader
except (ImportError, ), exc:
    def build_qt(clientId=0, reader=None, writer=None, socket=None):
        """ build_qt(clientId=0, ...) -> QThread not available.

        """
        raise exc
else:
    def build_qt(clientId=0, reader=None, writer=None, socket=None):        
        """ build_qt(clientId=0, ...) -> new ib connection with QThread reader

        """
        if reader is None:
            reader = QThreadReader()
        return build(clientId, reader, writer, socket)
