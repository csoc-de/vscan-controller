from typing import Any

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform


class GVMConfigs:
    def __init__(
        self,
        socket: UnixSocketConnection,
        transform: EtreeCheckCommandTransform,
        user: str,
        password: str,
    ) -> None:
        self.socket = socket
        self.transform = transform
        self.user: str = user
        self.password: str = password

    def get_configs(
        self,
        *,
        filter_string: str | None = None,
        trash: bool | None = None,
        details: bool | None = None,
        families: bool | None = None,
        preferences: bool | None = None,
        tasks: bool | None = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_scan_configs(
                filter_string=filter_string,
                trash=trash,
                details=details,
                families=families,
                preferences=preferences,
                tasks=tasks,
            )

    def import_scan_config(self, config: str) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.import_scan_config(config)
