from typing import Any, Optional

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform


class GVMPortLists:
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

    def get_port_lists(
            self,
            *,
            filter_string: Optional[str] = None,
            details: Optional[bool] = False,
            trash: Optional[bool] = False
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_port_lists(filter_string=filter_string, details=details, trash=trash)
