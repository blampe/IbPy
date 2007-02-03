#!/usr/bin/env python
""" ib.lib -> library for bits used elsewhere in this package.

"""
import logging
import os
import sys


maxint = sys.maxint
maxfloat = float(maxint)


logger_format = '%(asctime)s %(module)s.py:%(lineno)d %(levelname)-9.9s %(message)s'
logger_date_format = '%d-%b-%y %H:%M:%S'
logger_level = int(os.environ.get('IBPY_LOGLEVEL', logging.DEBUG))


def makelogger(name='ibpy', level=logger_level, format=logger_format,
               date_format=logger_date_format):
    """ makelogger(level) -> returns a logger all fixed up

    """
    logging.basicConfig(level=level, format=format, datefmt=date_format)
    return logging
logger = makelogger()


def getattrs(obj, seq):
    """ getattrs(obj, seq) -> get attributes named in seq from obj

    """
    values = [getattr(obj, k) for k in seq]
    try:
        return [v.lower() for v in values]
    except (AttributeError, ):
        return values


def setattrs(obj, mapping):
    """ setattrs(obj, mapping) -> add attributes from mapping to obj

    """
    del(mapping['self'])
    obj.__dict__.update(mapping)


def requireConnection(method):
    """ 

    """
    def check(self, *a, **b):
        try:
            peer = self.socket.getpeername()
        except (Exception, ), exc:
            logger.error('Socket not connected. %s', exc)
        else:
            return method(self, *a, **b)
    return check


def dispatchMethod(messageId):
    """

    """
    info = logger.info
    def notifyDeco(method):
        name = method.func_name
        def inner(self, *a, **b):
            info('%s.preDispatch(%s, ...)' % (name, messageId))
            self.preDispatch(messageId, *a, **b)
            result = method(self, *a, **b)
            info('%s.postDispatch(%s, ...)' % (name, messageId))
            self.postDispatch(messageId, *a, **b)
            return result
        return inner
    return notifyDeco


def requireServerVersion(op, version, message):
    """

    """
    def versionDeco(method):
        def inner(self, *a, **b):
            serverVersion = self.serverVersion
            if op(version, serverVersion):
                logger.error('%s; required %s have %s',
                             message, version, serverVersion)
            else:
                return method(self, *a, **b)
        return inner
    return versionDeco


try:
    from functools import partial
except (ImportError, ):
    class partial(object):
        """ partial(f, *a, **k) -> a callable object from a function

        """
        def __init__(self, fun, *args, **kwargs):
            self.fun = fun
            self.pending = args[:]
            self.kwargs = kwargs.copy()

        def __call__(self, *args, **kwargs):
            if kwargs and self.kwargs:
                kw = self.kwargs.copy()
                kw.update(kwargs)
            else:
                kw = kwargs or self.kwargs
            return self.fun(*(self.pending + args), **kw)
