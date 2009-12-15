#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines message types for the Receiver class.
#
# This module inspects the EWrapper class to build a set of Message
# types.  In creating the types, it also builds a registry of them
# that the Receiver class then uses to determine message types.
##

from ast import NodeVisitor, parse
from inspect import getsourcefile
from re import match

from ib.ext.AnyWrapper import AnyWrapper
from ib.ext.EWrapper import EWrapper
from ib.ext.EClientSocket import  EClientSocket


class SignatureAccumulator(NodeVisitor):
    def __init__(self):
	NodeVisitor.__init__(self)
	self.signatures = []

    def visit_FunctionDef(self, node):
	args = [arg.id for arg in node.args.args]
	self.signatures.append((node.name, args[1:]))

    def getSignatures(self):
	for filename in self.filenames:
            self.visit(parse(open(filename).read()))
	return self.filterSignatures()


class EClientSocketAccumulator(SignatureAccumulator):
    filenames = (getsourcefile(EClientSocket), )

    def filterSignatures(self):
        for name, args in self.signatures:
	    if match('(?i)req|cancel|place', name):
	        yield (name, args)


class EWrapperAccumulator(SignatureAccumulator):
    filenames = (getsourcefile(AnyWrapper), getsourcefile(EWrapper), )

    def filterSignatures(self):
        for name, args in self.signatures:
	    if match('(?!((?i)error.*))', name):
		yield (name, args)


##
# Dictionary that associates wrapper method names to the message class
# that should be instantiated for delivery during that method call.
registry = {}


class MessageType(type):
    """ MessageType -> simple metaclass to track Message subclasses

    As new Message subclasses are defined (see below), they are saved
    to the registry mapping.
    """
    def __init__(cls, name, bases, namespace):
        """ Constructor.

        @param name name of newly created type
        @param bases tuple of base classes for new type
        @param namespace dictionary with namespace of new type
        """
        setattr(cls, 'typeName', name)
	return
        try:
            registry[namespace['__assoc__']] = cls
        except (KeyError, ):
            pass


class Message(object):
    """ Base class for Message types.

    """
    __metaclass__ = MessageType
    __slots__ = []

    def __init__(self, **kwds):
        """ Constructor.

        @param **kwds keywords and values for instance
        """
        for name in self.__slots__:
            setattr(self, name, kwds.pop(name, None))
        assert not kwds

    def __len__(self):
        """ x.__len__() <==> len(x)

        """
        return len(self.keys())

    def __str__(self):
        """ x.__str__() <==> str(x)

        """
        name = self.typeName
        items = str.join(', ', ['%s=%s' % item for item in self.items()])
        return '<%s%s>' % (name, (' ' + items) if items else '')

    def items(self):
        """ List of message (slot, slot value) pairs, as 2-tuples.

        @return list of 2-tuples, each slot (name, value)
        """
        return zip(self.keys(), self.values())

    def values(self):
        """ List of instance slot values.

        @return list of each slot value
        """
        return [getattr(self, key, None) for key in self.keys()]

    def keys(self):
        """ List of instance slots.

        @return list of each slot.
        """
        return self.__slots__


class Error(Message):
    """ Specialized message type.

    The error family of method calls can't be built programmatically,
    so we define one here.
    """
    __assoc__ = 'error'
    __slots__ = ['id', 'errorCode', 'errorMsg']


def buildMessageTypes(seq, mapping, suffixes=('', ), bases=(Message, )):
    """ Construct message types and add to given mapping.

    @param seq pairs of method (name, arguments)
    @param mapping dictionary for adding new message types
    @param bases sequence of base classes for message types
    @return None
    """
    for name, args in seq:
	for suffix in suffixes:
	    typename = name[0].upper() + name[1:] + suffix
	    methname = name + suffix
	    typens = {'__slots__':args, '__assoc__':name}
	    mapping[typename] = msgtype = type(typename, bases, typens)
	    registry[methname] = msgtype


##
# Sequences for accessing the same values we use to create
# Message types.
wrapperMethods = list(EWrapperAccumulator().getSignatures())
clientSocketMethods = list(EClientSocketAccumulator().getSignatures())


# create message types in the module namespace from the EWrapper
# abstract class
buildMessageTypes(wrapperMethods, globals())

## create message types in the module namespace from the EClientSocket
# concrete class
buildMessageTypes(clientSocketMethods, globals(),
		  suffixes=('Before', 'After'))



def messageTypeNames():
    """ Builds set of message type names.

    @return set of all message type names as strings
    """
    return set([t.typeName for t in registry.values()])


del(AnyWrapper)
del(EWrapper)
del(EClientSocket)
