from typing import Dict

import traceback
import uvicorn

from gvm.protocols.gmp import GMP
from gvm.connections import UnixSocketConnection
from gvm.transforms import EtreeCheckCommandTransform


from app.config import GREENBONE_SOCKET_PATH,GREENBONE_USER, GREENBONE_PASSWORD, HOST, PORT
from app.gvm_tools.targets import GVMTargets
from app.routers.router import App

socket: UnixSocketConnection = UnixSocketConnection(path=GREENBONE_SOCKET_PATH)
transform: EtreeCheckCommandTransform = EtreeCheckCommandTransform()

def main():
    try:
        with GMP(connection=socket) as gmp:
            print(gmp.get_version())
        app = App(GVMTargets(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD))
        uvicorn.run(app.fastapi, host=HOST, port=PORT, log_level="info")
    except Exception as e:
        print(e)
        print(traceback.format_exc())

if __name__ == '__main__':
    main()