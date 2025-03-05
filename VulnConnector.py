from gvm.connections import TLSConnection
from gvm.connections import UnixSocketConnection
from gvm.connections import DebugConnection
from gvm.protocols.gmp import GMPv225 as Gmp
from gvm.transforms import EtreeTransform
import logging


class VulnConnector:

    def __init__(self, scanner_host=None, scanner_port=None, socket_path=None):
        self.gmp = Gmp
        #logging.basicConfig(level=logging.DEBUG)
        if socket_path is not None:
            # todo: check if socket exists in fs
            print("SOCK CONNECTION", socket_path)
            #path = '/opt/gvm/var/run/gvmd.sock'
            #connection = UnixSocketConnection(path=path)
            connection = UnixSocketConnection(path=socket_path)
        else:
            connection = TLSConnection(certfile=None, keyfile=None, hostname=scanner_host,
                                       port=scanner_port, password=None)
        transform = EtreeTransform()
        try:
            #connection = DebugConnection(connection=connection)
            self.gmp = Gmp(connection=connection, transform=transform)
        except ConnectionError:
            print("Could not connect to Scanner!")
