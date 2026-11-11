from typing import Any
from uuid import UUID

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform


class GVMSchedules:
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

    def get_schedule(self, schedule_id: str, tasks: bool | None = None) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_schedule(schedule_id, tasks=tasks)

    def get_schedules(
        self,
        *,
        filter_string: str | None = None,
        trash: bool | None = None,
        tasks: bool | None = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_schedules(filter_string=filter_string, trash=trash, tasks=tasks)

    def create_schedule(
        self,
        name: str,
        icalendar: str,
        timezone: str,
        *,
        comment: str | None = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.create_schedule(name, icalendar, timezone, comment=comment)

    def update_schedule(
        self,
        schedule_id: str | UUID,
        *,
        name: str | None = None,
        icalendar: str | None = None,
        timezone: str | None = None,
        comment: str | None = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.modify_schedule(
                schedule_id, name=name, icalendar=icalendar, timezone=timezone, comment=comment
            )

    def delete_schedule(self, schedule_id: str | UUID, *, ultimate: bool | None = False) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.delete_schedule(schedule_id, ultimate=ultimate)
