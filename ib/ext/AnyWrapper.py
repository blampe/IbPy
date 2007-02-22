#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translation source for AnyWrapper.
##

# Source file: AnyWrapper.java
# Target file: AnyWrapper.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.

from ib.aux.overloading import overloaded

class AnyWrapper(object):
    """ generated source for AnyWrapper

    """

    @overloaded
    def error(self, e):
        raise NotImplementedError()

    @error.register(object, str)
    def error_0(self, strval):
        raise NotImplementedError()

    @error.register(object, int, int, str)
    def error_1(self, id, errorCode, errorMsg):
        raise NotImplementedError()

    def connectionClosed(self):
        raise NotImplementedError()


