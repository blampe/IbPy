#!/usr/bin/env python
from ib.client import message
from ib.client.reader import Reader

from qt import PYSIGNAL, QObject, QThread, qApp


class QThreadReader(Reader, QThread):
    """ QThreadReader(...) -> a Qt thread for reading an IbPy socket

    This reader type is an alternate to the default Python threading.Thread 
    subtype.  By making QThread a superclass, instances can readily interoperate
    with the Qt framework.

    This type relies on Reader.run for its primary purpose of reading
    socket data.

    The connection object starts its reader on demand; neither the client nor 
    the instance should do that.
    """
    def __init__(self, readers, socket):
        Reader.__init__(self, readers, socket)
        QThread.__init__(self)


def messageTypes():
    """ messageTypes() -> returns a list of suitable IbPy message types

    This function returns a mapping of names and message types from the 
    IbPy.Message module.  These types are what IbPy instantiates and delivers
    as messages.
    """
    def isreader(cls):
        """ returns true if a class is a SocketReader subclass """
        basecls = message.MessageDecoder
        return issubclass(cls, basecls) and not cls is basecls

    def istype(cls):
        """ returns true if an object is a type """
        return isinstance(cls, (type, ))

    src = message.__dict__.values()
    types = [typ for typ in src if istype(typ) and isreader(typ)]
    return dict([(typ.__name__, typ) for typ in types])


def methodName(name):
    """ methodName(name) -> names a message-to-signal method

    """
    return 'messageSignalLink__%s' % (name, )


def slotName(name):
    """ slotName(name) -> names a slot method

    Clients define methods named 'slotAccount', 'slotTicker', 'slotPortfolio',
    etc.  This module uses that format for introspection of objects wishing to
    connect to the message transmitter.
    """
    return 'slot%s' % (name, )



## The second side of the link is the MessageTransmitter class.

## Instances of this type connect signals that they receive back to
## the parent for the magic of qt signal re-emitting.  The
## transmitMethod static method builder and the TransmitMethodInjector
## are used to create the methods suitable for callbacks from the IbPy
## socket reader defined above.


## The TransmitMethodInjector metaclass is useful because we can't add
## methods to instances (e.g., in __init__) because the sip/pyqt
## framework can't see them.  Adding the methods to the class as it's
## constructed allows us a resonable way to accomplish the goal.
## Plus, it's shorter and stops the need for lame reuse.


class TransmitMethodInjector(type):
    """ TransmitMethodInjector(...) -> linkage between IbPy msgs and Qt signals

    """
    def __new__(cls, name, bases, namespace):
        for msgname in messageTypes():
            namespace[methodName(msgname)] = cls.transmitMethod(msgname)
        return type(name, bases, namespace)

    def transmitMethod(name):
        """ transmitMethod(name) -> returns a method to emit socket messages
    
        """
        signal = PYSIGNAL(name)
    
        def transmit(self, msg):
            """ transmit(msg) -> emit the message as a qt signal
    
            """
            self.emit(signal, (msg, ))
        return transmit
    transmitMethod = staticmethod(transmitMethod)


## The metaclass builds methods for receiving IbPy messages.  When constructed,
## instances register these methods with the sessions broker object to receive
## the IbPy messages.  The methods then emit signals with the messages as their
## argument.


class MessageTransmitter(QObject):
    """ MessageTransmitter(...) -> proxies IbPy messages to Qt signals

    """
    __metaclass__ = TransmitMethodInjector

    def __init__(self, parent):
        QObject.__init__(self, parent)
        for name, msg in messageTypes().items():
            parent.connect(self, PYSIGNAL(name), parent, PYSIGNAL(name))
            slot = getattr(self, methodName(name), None)


## The third side of the link is for widgets that want to react to
## messages.

## Widgets can call this connect function as a convenience for
## connecting to the signals from IbPy.  The side effect is that the
## signal source is hidden from the client.

def connect(widget, parent=None):
    """ connect(widget) -> connect a widgets known slots to the main gui widget

    """
    if not parent:
        parent = qApp.mainWidget()

    for name in messageTypes():
        meth = getattr(widget, slotName(name), None)
        if meth:
            signal = PYSIGNAL(name)
            parent.connect(parent, signal, meth)


