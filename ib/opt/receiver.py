#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Receiver class to handle inbound data.
#
# The Receiver class is built programatically at runtime.  Message
# types are defined in the ib.opt.message module, and those types are
# used to construct methods on the Receiver class during its
# definition.  Refer to the ReceiverType metaclass and the
# ib.opt.message module more information.
#
##
from Queue import Queue, Empty

from ib.lib.overloading import overloaded
from ib.lib.logger import logger
from ib.opt.message import registry, wrapperMethods


def messageMethod(name, argnames):
    """ Creates method for dispatching messages.

    @param name name of method as string
    @param argnames list of method argument names
    @return newly created method (as closure)
    """
    def inner(self, *args):
        params = dict(zip(argnames, args))
        self.dispatch(name, params)
    inner.__name__ = name
    return inner


class ReceiverType(type):
    """ Metaclass to add EWrapper methods to Receiver class.

    When the Receiver class is defined, this class adds all of the
    wrapper methods to it.
    """
    def __new__(cls, name, bases, namespace):
        """ Creates a new type.

        @param name name of new type as string
        @param bases tuple of base classes
        @param namespace dictionary with namespace for new type
        @return generated type
        """
        for methodname, methodargs in wrapperMethods():
            namespace[methodname] = messageMethod(methodname, methodargs)
        return type(name, bases, namespace)


class Receiver(object):
    """ Receiver -> dispatches messages to interested callables

    Instances implement the EWrapper interface by way of the
    metaclass.
    """
    __metaclass__ = ReceiverType

    def __init__(self, listeners=None, types=None):
        """ Initializer.

        @param listeners=None mapping of existing listeners
        @param types=None method name to message type lookup
        """
        self.listeners = listeners if listeners else {}
        self.types = types if types else registry
        self.logger = logger()

    def dispatch(self, name, mapping):
        """ Send message to each listener.

        @param name method name
        @param mapping values for message instance
        @return None
        """
        try:
            messagetype = self.types[name]
            listeners = self.listeners[self.key(messagetype)]
        except (KeyError, ):
            pass
        else:
            message = messagetype(**mapping)
            for listener in listeners:
                try:
                    listener(message)
                except (Exception, ):
                    self.unregister(listener, messagetype)
                    errmsg = ("Exception in message dispatch.  "
                              "Handler '%s' unregistered for '%s'")
                    self.logger.exception(errmsg, self.key(listener), name)

    def iterator(self, *types):
	""" Create and return a function for iterating over messages.

        @param *types zero or more message types to associate with listener
        @return function that yields messages
	"""
	queue = Queue()
	closed = []
	def messageGenerator(block=True, timeout=0.1):
	    while True:
		try:
		    yield queue.get(block=block, timeout=timeout)
		except (Empty, ):
		    if closed:
			break
	self.register(closed.append, 'ConnectionClosed')
	if types:
	    self.register(queue.put, *types)
	else:
	    self.registerAll(queue.put)
	return messageGenerator

    def register(self, listener, *types):
        """ Associate listener with message types created by this Receiver.

        @param listener callable to receive messages
        @param *types zero or more message types to associate with listener
        @return True if associated with one or more handler; otherwise False
        """
        count = 0
        for messagetype in types:
            key = self.key(messagetype)
            listeners = self.listeners.setdefault(key, [])
            if listener not in listeners:
                listeners.append(listener)
                count += 1
        return count > 0

    def registerAll(self, listener):
        """ Associate listener with all messages created by this Receiver.

        @param listener callable to receive messages
        @return True if associated with one or more handler; otherwise False
        """
        return self.register(listener, *self.types.values())

    def unregister(self, listener, *types):
        """ Disassociate listener with message types created by this Receiver.

        @param listener callable to no longer receive messages
        @param *types zero or more message types to disassociate with listener
        @return True if disassociated with one or more handler; otherwise False
        """
        count = 0
        for messagetype in types:
            try:
                listeners = self.listeners[self.key(messagetype)]
            except (KeyError, ):
                pass
            else:
                if listener in listeners:
                    listeners.remove(listener)
                    count += 1
        return count > 0

    def unregisterAll(self, listener):
        """ Disassociate listener with all messages created by this Receiver.

        @param listener callable to no longer receive messages
        @return True if disassociated with one or more handler; otherwise False
        """
        return self.unregister(listener, *self.types.values())

    @staticmethod
    def key(obj):
        """ Generates lookup key for given object.

        @param obj any object
        @return obj name or string representation
        """
        try:
            return obj.__name__
        except (AttributeError, ):
            return str(obj)

    @overloaded
    def error(self, e):
        """ Dispatch an error generated by the reader.

        Error message types can't be associated in the default manner
        with this family of methods, so we define these three here
        by hand.

        @param e some error value
        @return None
        """
        self.dispatch('error', dict(errorMsg=e))

    @error.register(object, str)
    def error_0(self, strval):
        """ Dispatch an error given a string value.

        @param strval some error value as string
        @return None
        """
        self.dispatch('error', dict(errorMsg=strval))

    @error.register(object, int, int, str)
    def error_1(self, id, errorCode, errorMsg):
        """ Dispatch an error given an id, code and message.

        @param id error id
        @param errorCode error code
        @param errorMsg error message
        @return None
        """
        params = dict(id=id, errorCode=errorCode, errorMsg=errorMsg)
        self.dispatch('error', params)
