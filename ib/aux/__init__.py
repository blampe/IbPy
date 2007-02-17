#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" just enough auxiliary bits to make the translated code work

"""
import socket
import struct
import sys
import threading


def synchronized(lock):
    """ synchronization decorator

    from http://wiki.python.org/moin/PythonDecoratorLibrary
    """
    def wrapper(func):
        def inner(*args, **kwds):
            lock.acquire()
            try:
                return func(*args, **kwds)
            finally:
                lock.release()
        return inner
    return wrapper


class Boolean(object):
    """ partial implementation of java Boolean type

    """
    def __init__(self, value):
        self.value = value

    def booleanValue(self):
        """ the value of this instance (a bool)

        @return True or False
        """
        return self.value

    @classmethod
    def valueOf(cls, text):
        """ creates an instance of this class with a bool value

        @param cls this class
        @param text string
        @return instance of cls
        """
        value = str(text).lower() == 'true'
        return cls(value)


class Cloneable(object):
    """ stub for the Cloneable java interface

    some of the translated code implements the java Cloneable
    interface, but its methods are never used.  we provide this class
    for subtyping, and will implement methods as needed later.
    """


class DataInputStream(object):
    """ partial implementation of the java DataInputStream type

    """
    def __init__(self, stream):
        self.recv = stream.recv

    def readByte(self, unpack=struct.unpack):
        """ reads a byte from the contained stream

        keyword arguments are bound to module globals for faster
        access.

        @return string read from stream
        """
        return unpack('!b', self.recv(1))[0]


class DataOutputStream(object):
    """ partial implementation of the java DataOutputStream type

    """
    def __init__(self, stream):
        self.send = stream.send

    def write(self, data, pack=struct.pack, eol=struct.pack('!b', 0)):
        """ writes data to the contained stream

        keyword arguments are bound to module globals for faster
        access.

        @param data string to send, or 0
        @return None
        """
        send = self.send
        if data == 0:
            send(eol)
        else:
            for char in data:
                send(pack('!c', char))


class Double(float):
    """ partial implementation of java Double type

    """
    MAX_VALUE = sys.maxint

    @staticmethod
    def parseDouble(text):
        """ returns python float from string

        """
        return float(text)


class Integer(int):
    """ partial implementation of java Integer type

    """
    MAX_VALUE = sys.maxint

    @staticmethod
    def parseInt(text):
        """ returns python int from string

        """
        return int(text)

    @staticmethod
    def parseLong(text):
        """ returns python long from string

        """
        return long(text)


class Socket(socket.socket):
    """ partial implementation of the java Socket type.

    """
    def __init__(self, host, port):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def getInputStream(self):
        """ returns this instance, which has a send method

        """
        return self

    def getOutputStream(self):
        """ returns this instance, which has a recv method

        """
        return self


class StringBuffer(list):
    """ partial implementation of the java StringBuffer type

    translated code uses instances of this type to build up strings.
    the list base type provides the append method.

    """
    def __str__(self, join=str.join, chr=chr):
        """ the string value of this instance

        keyword arguments are bound to module globals for faster
        access.

        @return string from characters contained in this instance
        """
        return join('', [chr(v) for v in self])


class Thread(threading.Thread):
    """ partial implementationof the java Thread type

    """
    def __init__(self, name, parent, dis):
        threading.Thread.__init__(self, name=name)
        self.setDaemon(True)

    def isInterrupted(self):
        """ returns False, which signals the reader to keep reading

        """
        return False

    def interrupt(self):
        """ no-op; python threads are not directly interruptible

        """
        return False
