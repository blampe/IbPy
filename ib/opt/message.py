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
from ib.lib import toTypeName


class SignatureAccumulator(NodeVisitor):
    """

    """
    def __init__(self, classes):
        NodeVisitor.__init__(self)
        self.signatures = []
        for filename in (getsourcefile(cls) for cls in classes):
            self.visit(parse(open(filename).read()))

    def visit_FunctionDef(self, node):
        args = [arg.id for arg in node.args.args]
        self.signatures.append((node.name, args[1:]))


class EClientSocketAccumulator(SignatureAccumulator):
    def getSignatures(self):
        for name, args in self.signatures:
            if match('(?i)req|cancel|place', name):
                yield (name, args)


class EWrapperAccumulator(SignatureAccumulator):
    def getSignatures(self):
        for name, args in self.signatures:
            if match('(?!((?i)error.*))', name):
                yield (name, args)


##
# Dictionary that associates wrapper method names to the message class
# that should be instantiated for delivery during that method call.
registry = {}


def messageTypeNames():
    """ Builds set of message type names.

    @return set of all message type names as strings
    """
    def typeNames():
        for types in registry.values():
            for typ in types:
                yield typ.typeName
    return set(typeNames())


class Message(object):
    """ Base class for Message types.

    """
    __slots__ = ()

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
    __slots__ = ('id', 'errorCode', 'errorMsg')


def buildMessageRegistry(seq, suffixes=[''], bases=(Message, )):
    """ Construct message types and add to given mapping.

    @param seq pairs of method (name, arguments)
    @param bases sequence of base classes for message types
    @return None
    """
    for name, args in sorted(seq):
        for suffix in suffixes:
            typename = toTypeName(name) + suffix
            typens = {'__slots__':args, '__assoc__':name, 'typeName':name}
            msgtype = type(typename, bases, typens)
            if name in registry:
                registry[name] = registry[name] + (msgtype, )
            else:
                registry[name] = (msgtype, )




eWrapperAccum = EWrapperAccumulator((AnyWrapper, EWrapper))
eClientAccum = EClientSocketAccumulator((EClientSocket, ))

wrapperMethods = list(eWrapperAccum.getSignatures())
clientSocketMethods = list(eClientAccum.getSignatures())
errorMethods = [('error', Error.__slots__), ]

buildMessageRegistry(wrapperMethods)
buildMessageRegistry(clientSocketMethods, suffixes=('Pre', 'Post'))
buildMessageRegistry(errorMethods)

def initModule():
    target = globals()
    for messageTypes in registry.values():
        for messageType in messageTypes:
            target[messageType.typeName] = messageType

try:
    initModule()
except (NameError, ):
    pass
else:
    del(initModule)


del(AnyWrapper)
del(EWrapper)
del(EClientSocket)
del(eWrapperAccum)
del(eClientAccum)
