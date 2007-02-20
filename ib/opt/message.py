#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ib.opt.message -> defines message types for the Receiver class.

This module inspects the EWrapper class to build a set of Message
types.  In creating the types, it also builds a registry of them that
the Receiver class uses to determine message types to instantiate and
deliver.
"""
from functools import partial
from inspect import getargspec
from types import MethodType

from ib.ext.EWrapper import EWrapper


##
## maps wrapper method names to the message class that can be
## instantiated for delivery by the named method.
##
registry = {}


class MessageType(type):
    """ MessageType -> simple metaclass to track Message subclasses

    As new Message subclasses are defined (see below), they are saved
    to the registry mapping.
    """
    def __init__(cls, name, bases, namespace):
        try:
            registry[namespace['__assoc__']] = cls
        except (KeyError, ):
            pass


class Message(object):
    """ Message -> base type for message instances

    """
    __metaclass__ = MessageType
    __slots__ = []

    def __init__(self, **kwds):
        for name in self.__slots__:
            setattr(self, name, kwds.pop(name, None))
        assert not kwds

    def __str__(self):
        name = self.__class__.__name__
        items = str.join(', ', ['%s=%s' % item for item in self.items()])
        return '<%s message%s>' % (name, ' ' + items if items else '')

    def items(self):
        """ list of message's (slot, slot value) pairs, as 2-tuples

        """
        return zip(self.keys(), self.values())

    def values(self):
        """ list of message's slot values

        """
        return [getattr(self, key) for key in self.keys()]

    def keys(self):
        """ list of message's slots

        """
        return self.__slots__


class Error(Message):
    """ Error -> specialized message type

    The error family of method calls can't be built programmatically,
    so we define one here.
    """
    __assoc__ = 'error'
    __slots__ = ['id', 'errorCode', 'errorMsg']


def isWrapperMethod(name, value):
    """ predicate for wrapper methods

    @param name name of class attribute as string
    @param value value of class attribute; any object
    @return True if wrapper method
    """
    return (not name.startswith('_') and
            not name.startswith('error') and
            isinstance(value, MethodType))


def selectWrapperMethods(cls):
    """ wrapper methods of a class

    @param cls class object to inspect
    @return list of two-tuples, each (name, method)
    """
    items = [(name, getattr(cls, name)) for name in dir(cls)]
    items =  [(name, value) for name, value in items
                if isWrapperMethod(name, value)]
    return [(name, getargspec(value)[0][1:]) for name, value in items]


def buildMessageTypes(wrapper, mapping, *bases):
    """ construct message types and add to given mapping

    @param wrapper class object to inspect for methods
    @param mapping dictionary for adding new message types
    @param bases sequence of base classes for message types
    @return None;
    """
    for name, args in selectWrapperMethods(wrapper):
        typename = name[0].upper() + name[1:]
        typens = {'__slots__':args, '__assoc__':name}
        mapping[typename] = type(typename, bases, typens)


##
## create message types in the module namespace from the EWrapper
## abstract class
##
buildMessageTypes(EWrapper, globals(), Message)


##
## define a method so other modules can use the same mappings
## we have.
wrapperMethods = partial(selectWrapperMethods, EWrapper)
