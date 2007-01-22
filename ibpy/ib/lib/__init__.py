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
    values = [getattr(obj, k) for k in seq]
    try:
        return [v.lower() for v in values]
    except (AttributeError, ):
        return values


def setattrs(obj, mapping):
    """ setattrs(object, mapping) -> add attributes from mapping to obj

    """
    del(mapping['self'])
    obj.__dict__.update(mapping)


def onlyConnected(method):
    def connectionChecker(self, *a, **b):
        try:
            peer = self.socket.getpeername()
        except (Exception, ), exc:
            logger.error('Socket not connected. %s', exc)
        else:
            return method(self, *a, **b)
    return connectionChecker


def notifyEnclosure(messageId):
    def notifyDeco(method):
        def innerEnclosure(self, *a, **b):
            logger.info('%s.preDispatch(%s, ...)' % (method.func_name, messageId))
            self.preDispatch(messageId, *a, **b)
            result = method(self, *a, **b)
            logger.info('%s.postDispatch(%s, ...)' % (method.func_name, messageId))
            self.postDispatch(messageId, *a, **b)
            return result
        return innerEnclosure
    return notifyDeco


def restrictServerVersion(op, version, message):
    def allowServerVersionDeco(method):
        def serverVersionChecker(self, *a, **b):
            if op(version, self.serverVersion):
                logger.error('%s; required %s have %s', message, version, self.serverVersion)
            else:
                return method(self, *a, **b)
        return serverVersionChecker
    return allowServerVersionDeco
