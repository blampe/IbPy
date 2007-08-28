#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translation source for AnyWrapperMsgGenerator.
##

# Source file: AnyWrapperMsgGenerator.java
# Target file: AnyWrapperMsgGenerator.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes made to this file will be lost.

from ib.lib import cmattr
from ib.lib.overloading import overloaded

class AnyWrapperMsgGenerator(object):
    """ generated source for AnyWrapperMsgGenerator

    """

    @cmattr
    @overloaded
    def error(cls, ex):
        return "Error - " + ex.message

    @cmattr
    @error.register(type, str)
    def error_0(cls, strval):
        return strval

    @cmattr
    @error.register(type, int, int, str)
    def error_1(cls, id, errorCode, errorMsg):
        err = str(id)
        err += " | "
        err += str(errorCode)
        err += " | "
        err += errorMsg
        return err

    @classmethod
    def connectionClosed(cls):
        return "Connection Closed"


