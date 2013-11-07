#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Just enough auxiliary bits to make the translated code work.
#
# This package provides the support necessary to use the translated
# code.  The configuration modules used in translation take care of
# many semantic differences between Java and Python, while this
# package provides the rest.
##

import copy
import functools
import socket
import struct
import sys

def toTypeName(value):
    return '%s%s' % (value[0].upper(), value[1:])


def maybeName(obj):
    """ Returns an object's __name__ attribute or it's string representation.

    @param obj any object
    @return obj name or string representation
    """
    try:
        return obj.__name__
    except (AttributeError, ):
        return str(obj)


class classmethod_(classmethod):
    """ Classmethod that provides attribute delegation.

    """
    def __init__(self, func):
        classmethod.__init__(self, func)
        self.func = func

    def __getattr__(self, name):
        return getattr(self.func, name)


def synchronized(lock):
    """ Synchronization decorator.

    from http://wiki.python.org/moin/PythonDecoratorLibrary

    @param lock Lock or RLock instance
    @return decorator that provides automatic locking
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwds):
            lock.acquire()
            try:
                return func(*args, **kwds)
            finally:
                lock.release()
        return inner
    return wrapper


class Boolean(object):
    """ Partial implementation of Java Boolean type.

    """
    def __init__(self, value):
        """ Constructor.

        @param value bool instance, True or False
        """
        self.value = value

    def booleanValue(self):
        """ The value of this instance (a bool).

        @return True or False
        """
        return self.value

    @classmethod
    def valueOf(cls, text):
        """ Creates an instance of this class with a bool value.

        @param cls this class
        @param text string
        @return instance of cls
        """
        value = str(text).lower() == 'true'
        return cls(value)


class Cloneable(object):
    """ Stub for the Cloneable Java interface.

    Some of the translated code implements the Java Cloneable
    interface, but its methods are never used.  We provide this class
    for sub typing, and will implement methods as needed later.
    """
    def clone(self):
        return copy.copy(self)


class DataInputStream(object):
    """ Partial implementation of the Java DataInputStream type.

    """
    def __init__(self, stream):
        """ Constructor.

        @param stream any object with recv method
        """
        self.stream = stream
        self.recv = stream.recv

    def readByte(self, unpack=struct.unpack):
        """ Reads a byte from the contained stream.

        @return string read from stream
        """
        return unpack('!b', self.recv(1))[0]


class DataOutputStream(object):
    """ Partial implementation of the Java DataOutputStream type

    """
    def __init__(self, stream):
        """ Constructor.

        @param stream any object with send method
        """
        self.send = stream.send

    def write(self, data, pack=struct.pack, eol=struct.pack('!b', 0)):
        """ Writes data to the contained stream.

        @param data string to send, or 0
        @return None
        """
        send = self.send
        if data == 0:
            send(eol)
        else:
            for char in data:
                if sys.version_info[0] > 2:
                    char = char.encode('utf-8')
                send(pack('!c', char))


class Double(float):
    """ Partial implementation of Java Double type.

    """
    ##
    # sentinel value used by the socket writer
    MAX_VALUE = sys.maxint

    @staticmethod
    def parseDouble(text):
        """ Float double (float) from string.

        @param text value to parse
        @return float instance
        """
        return float(text or 0)


class Integer(int):
    """ Partial implementation of Java Integer type.

    """
    ##
    # sentinel value used by the socket writer
    MAX_VALUE = sys.maxint

    @staticmethod
    def parseInt(text):
        """ Int from string.

        @param text value to parse
        @return int instance
        """
        return int(text or 0)

    @staticmethod
    def parseLong(text):
        """ Long from string.

        @param text value to parse
        @return long instance
        """
        return long(text or 0)


##
# The generated code uses Longs just like Integers, so we use an alias
# instead of a subclass (for now).
Long = Integer


class Socket(socket.socket):
    """ Partial implementation of the Java Socket type.

    """
    def __init__(self, host, port):
        """ Constructor; attempts connection immediately.

        @param host hostname as string
        @param port port number as integer
        """
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def getInputStream(self):
        """ Returns this instance, which has a send method.

        """
        return self

    def getOutputStream(self):
        """ Returns this instance, which has a recv method.

        """
        return self
    
    def disconnect(self):
        self.shutdown(socket.SHUT_RDWR)
        self.close()

    def isConnected(self):
        try:
            throwaway = self.getpeername()
            return True
        except (socket.error, ), ex:
            return False
        

class StringBuffer(list):
    """ Partial implementation of the Java StringBuffer type

    Translated code uses instances of this type to build up strings.
    The list base type provides the append method.
    """
    def __str__(self, join=str.join, chr=chr):
        """ the string value of this instance

        @return string from characters contained in this instance
        """
        return join('', [chr(v) for v in self])


if 'qt' in sys.modules:
    from qt import QThread

    class ThreadType(QThread):
        """ Partial implementation of Java Thread type, based on Qt3 QThread.

        """
        def __init__(self, name):
            """ Constructor.

            @param name ignored
            """
            QThread.__init__(self)

        def interrupt(self):
            """ Stop this thread (by call to terminate).

            """
            return self.terminate()

        def isInterrupted(self):
            """ Check state of thread.

            @return True if thread is finished
            """
            return self.finished()

        def setDaemon(self, value):
            """ No-op.

            @param value ignored
            @return None
            """

        def setName(self, value):
            """ No-op.

            @param value ignored
            @return None
            """



elif 'PyQt4' in sys.modules:
    from PyQt4.QtCore import QThread

    class ThreadType(QThread):
        """ Partial implementation of Java Thread type, based on Qt4 QThread.

        """
        def __init__(self, name):
            """ Constructor.

            @param name ignored
            """
            QThread.__init__(self)

        def interrupt(self):
            """ stop this thread (by call to exit)

            """
            return self.exit()

        def isInterrupted(self):
            """ check state of thread

            @return True if thread is finished
            """
            return self.isFinished()

        def setDaemon(self, value):
            """ No-op.

            @param value ignored
            @return None
            """

        def setName(self, value):
            """ sets the name of this QObject

            @param value name of object as string
            @return None
            """
            self.setObjectName(value)


else:
    import threading

    class ThreadType(threading.Thread):
        """ Partial implementation of Java Thread type, based on Python Thread.

        """
        def __init__(self, name):
            """ Constructor.

            @param name name of this thread
            """
            threading.Thread.__init__(self, name=name)
            self.setDaemon(True)

        def interrupt(self):
            """ No-op; Python threads are not directly interruptible.

            """
            return False

        def isInterrupted(self):
            """ Check state of thread (always False).

            @return False
            """
            return False


class Thread(ThreadType):
    """ Thread parent type, based on available framework

    """
    def __init__(self, name, parent, dis):
        """ Constructor.

        @param name name of this thread
        @param parent ignored
        @param dis ignored
        """
        ThreadType.__init__(self, name=name)


    def term(self):
        def isInterrupted():
            print 'down town'
            return True
        self.isInterrupted = isInterrupted
        self.m_dis.stream.shutdown(socket.SHUT_RDWR)
        self.m_dis.stream.close()
