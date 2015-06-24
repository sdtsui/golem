import logging
import time

from golem.network.p2p.NetConnState import NetConnState
from golem.core.variables import LONG_STANDARD_SIZE

logger = logging.getLogger(__name__)

class NetAndFilesConnState( NetConnState ):
    ############################
    def __init__( self, server = None):
        NetConnState.__init__( self, server )

        self.fileMode = False
        self.fileConsumer = None

        self.dataMode = False
        self.dataConsumer = None

        self.fileProducer = None

    ############################
    def _interpret(self, data):

        self.session.lastMessageTime = time.time()

        if self.fileMode:
            self.fileDataReceived( data )
            return

        if self.dataMode:
            self.resultDataReceived(data)
            return

        NetConnState._interpret(self, data)

    ############################
    def fileDataReceived( self, data  ):
        assert self.fileConsumer
        assert len( data ) >= LONG_STANDARD_SIZE

        self.fileConsumer.dataReceived( data )

    ############################
    def resultDataReceived( self, data ):
        assert self.dataConsumer
        assert len( data ) >= LONG_STANDARD_SIZE

        self.dataConsumer.dataReceived( data )

    ############################
    def clean(self):
        if self.dataConsumer is not None:
            self.dataConsumer.close()

        if self.fileConsumer is not None:
            self.fileConsumer.close()

        if self.fileProducer is not None:
            self.fileProducer.close()