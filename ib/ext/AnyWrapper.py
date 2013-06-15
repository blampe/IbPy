#!/usr/bin/env python
""" generated source for module AnyWrapper """
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from abc import ABCMeta, abstractmethod
from ib.lib.overloading import overloaded
# 
#  * AnyWrapper.java
#  *
#  
# package: com.ib.client
class AnyWrapper(object):
    """ generated source for interface AnyWrapper """
    __metaclass__ = ABCMeta
    @abstractmethod
    @overloaded
    def error(self, e):
        """ generated source for method error """

    @abstractmethod
    @error.register(object, str)
    def error_0(self, strval):
        """ generated source for method error_0 """

    @abstractmethod
    @error.register(object, int, int, str)
    def error_1(self, id, errorCode, errorMsg):
        """ generated source for method error_1 """

    @abstractmethod
    def connectionClosed(self):
        """ generated source for method connectionClosed """

