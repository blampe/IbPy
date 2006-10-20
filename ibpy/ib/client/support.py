#!/usr/bin/env python
from ib import lib


logger = lib.logger()


def allowOnlyConnected(method):
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
            self.preDispatch(messageId)
            method(self, *a, **b)
            self.postDispatch(messageId)
        return innerEnclosure
    return notifyDeco


def restrictServerVersion(op, version, message):
    def allowServerVersionDeco(method):
        def serverVersionChecker(self, *a, **b):
            if op(version, self.serverVersion):
                logger.error('%s; server version required %s', message, version)
            else:
                return method(self, *a, **b)
        return serverVersionChecker
    return allowServerVersionDeco
