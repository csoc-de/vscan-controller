from typing import Any, Optional

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform


class GVMScanners:
    def __init__(
            self,
            socket: UnixSocketConnection,
            transform: EtreeCheckCommandTransform,
            user: str,
            password: str
    ) -> None:
        self.socket = socket
        self.transform = transform
        self.user: str = user
        self.password: str = password

    def get_scanners(
            self,
            *,
            filter_string: Optional[str] = None,
            trash: Optional[bool] = None,
            details: Optional[bool] = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_scanners(filter_string=filter_string, trash=trash, details=details)
