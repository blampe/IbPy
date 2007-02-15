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

    myLock = Lock()

# Example usage:
if 0:
    from threading import Lock
    myLock = Lock()

    @synchronized(myLock)
    def critical1(*args):
        # Interesting stuff goes here.
        pass

    @synchronized(myLock)
    def critical2(*args):
        # Other interesting stuff goes here.
        pass


# various helpers

class Integer(int):
    MAX_VALUE = sys.maxint

class Double(float):
    MAX_VALUE = sys.maxint

class Cloneable(object):
    pass

class Socket(object):
    pass

class DataOutputStream(object):
    pass


class DataInputStream(object):
    pass

class Thread(object):
    pass
