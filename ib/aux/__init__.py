# from http://wiki.python.org/moin/PythonDecoratorLibrary
import sys


def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap


# various helpers

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
    def append(self, value):
        pass

class Boolean(object):
    def valueOf(value):
        pass

    def booleanValue(self):
        pass

class Socket(object):
    def __init__(self, host, port):
        pass

    def getInputStream(self):
        pass

    def getOutputStream(self):
        pass


class DataOutputStream(object):
    def __init__(self, stream):
        pass

    def write(self, value):
        pass


class DataInputStream(object):
    def __init__(self, stream):
        pass

    def readByte(self):
        pass


class Thread(object):
    def isInterrupted(self):
        pass

