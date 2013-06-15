#!/usr/bin/env python
""" generated source for module AnyWrapperMsgGenerator """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib import classmethod_ as classmethod
from ib.lib.overloading import overloaded
# package: com.ib.client
class AnyWrapperMsgGenerator(object):
    """ generated source for class AnyWrapperMsgGenerator """
    @classmethod
    @overloaded
    def error(cls, ex):
        """ generated source for method error """
        return "Error - " + ex

    @classmethod
    @error.register(object, str)
    def error_0(cls, strval):
        """ generated source for method error_0 """
        return strval

    @classmethod
    @error.register(object, int, int, str)
    def error_1(cls, id, errorCode, errorMsg):
        """ generated source for method error_1 """
        err = str(id)
        err += " | "
        err += str(errorCode)
        err += " | "
        err += errorMsg
        return err

    @classmethod
    def connectionClosed(cls):
        """ generated source for method connectionClosed """
        return "Connection Closed"

