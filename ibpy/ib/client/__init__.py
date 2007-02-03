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

def build_qt3(clientId=0, reader=None, writer=None, socket=None):        
    """ build_qt3(clientId=0, ...) -> new ib connection with Qt3 QThread reader

    """
    from ib.client.qthreadreader3 import QThreadReader        
    if reader is None:
        reader = QThreadReader()
    return build(clientId, reader, writer, socket)


def build_qt4(clientId=0, reader=None, writer=None, socket=None):        
    """ build_qt4(clientId=0, ...) -> new ib connection with Qt4 QThread reader

    """
    from ib.client.qthreadreader4 import QThreadReader        
    if reader is None:
        reader = QThreadReader()
    return build(clientId, reader, writer, socket)

