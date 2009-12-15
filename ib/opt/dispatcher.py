#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Dispatcher class to send messages to registered listeners.
#
##
from Queue import Queue, Empty

from ib.lib.logger import logger
from ib.opt.message import registry


class Dispatcher(object):
    """

    """
    def __init__(self, listeners=None, types=None):
        """ Initializer.

        @param listeners=None mapping of existing listeners
        @param types=None method name to message type lookup
        """
        self.listeners = listeners if listeners else {}
        self.types = types if types else registry
        self.logger = logger()

    def __call__(self, name, mapping):
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
        """ Associate listener with message types created by this Dispatcher.

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
        """ Associate listener with all messages created by this Dispatcher.

        @param listener callable to receive messages
        @return True if associated with one or more handler; otherwise False
        """
        return self.register(listener, *self.types.values())

    def unregister(self, listener, *types):
        """ Disassociate listener with message types created by this Dispatcher.

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
        """ Disassociate listener with all messages created by this Dispatcher.

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
