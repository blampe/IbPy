#!/usr/bin/env python
from ib.client.reader import Reader
from ib.lib import partial

from PyQt4.QtCore import QThread, SIGNAL



class QThreadReader(Reader, QThread):
    """ QThreadReader(...) -> a Qt thread for reading an IbPy socket

    This reader type is an alternate to the default Python threading.Thread 
    subtype.  By making QThread a superclass, instances can readily interoperate
    with the Qt framework.

    This type relies on Reader.run for its primary purpose of reading
    socket data.

    The connection object starts its reader on demand; neither the client nor 
    the instance should do that.

    Instances of this type register themselves with each type of
    message decoder.  When run, the decoder calls this thread, which
    then emits the message as a signal.
    """
    def __init__(self, decoders=None):
        Reader.__init__(self, decoders)
        QThread.__init__(self)
        for decoder in self.decoders.values():
            decoder.listeners[1].append(partial(self, decoder=decoder))

    def __call__(self, message, decoder):
        self.emit(SIGNAL(decoder.__class__.__name__), message)

