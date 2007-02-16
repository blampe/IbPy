#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
from struct import pack, unpack
eof = pack('!i', 0)[3]


def synchronized(lock):
    """ synchronization decorator

    from http://wiki.python.org/moin/PythonDecoratorLibrary
    """
    def wrapper(f):
        def inner(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return inner
    return wrapper


class Boolean(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def valueOf(cls, value):
        return cls(str(value).lower() == 'true')

    def booleanValue(self):
        return self.value


class Integer(int):
    MAX_VALUE = sys.maxint

    @staticmethod
    def parseInt(value):
        return int(value)

    @staticmethod
    def parseLong(value):
        return long(value)


class Double(float):
    MAX_VALUE = sys.maxint

    @staticmethod
    def parseDouble(value):
        return float(value)


class Cloneable(object):
    pass


class StringBuffer(object):
    def __init__(self):
        self.seq = []

    def append(self, value):
        self.seq.append(value)

    def __str__(self):
        s = str.join('', [chr(v) for v in self.seq])
        return s


class Socket(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def getInputStream(self):
        return self.socket

    def getOutputStream(self):
        return self.socket





class DataOutputStream(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        send = self.stream.send
        for k in str(data):
            send(pack('!i', ord(k))[3])
        send(eof)


class DataInputStream(object):
    def __init__(self, stream):
        self.stream = stream

    def readByte(self):
        bite = self.stream.recv(1)
        bite = unpack('!b', bite)[0]
        return bite


class Thread(threading.Thread):
    def __init__(self, name, arg1, arg2):
        threading.Thread.__init__(self, name=name)
        self.setName(name)
        self.m_parent = arg1
        self.m_dis = arg2
        self.setDaemon(True)

    def isInterrupted(self):
        return False

