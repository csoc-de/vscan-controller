from typing import Any, Optional, Union, Sequence, Mapping
from uuid import UUID

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform
from gvm.utils import SupportsStr

from app.models.tasks import HostsOrdering


class GVMTasks:
    def __init__(self, socket: UnixSocketConnection, transform: EtreeCheckCommandTransform, user: str,
                 password: str) -> None:
        self.socket = socket
        self.transform = transform
        self.user: str = user
        self.password: str = password

    def get_task(self, task_id: str) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_task(task_id)

    def get_tasks(
            self, filter_string: Optional[str] = None,
            trash: Optional[bool] = False,
            details: Optional[bool] = None
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_tasks(filter_string=filter_string, trash=trash, details=details)

    def create_task(
            self,
            name: str,
            config_id: Union[str, UUID],
            target_id: Union[str, UUID],
            scanner_id: Union[str, UUID],
            *,
            alterable: Optional[bool] = None,
            hosts_ordering: Optional[HostsOrdering] = None,
            schedule_id: Optional[Union[str, UUID]] = None,
            alert_ids: Optional[Sequence[Union[str, UUID]]] = None,
            comment: Optional[str] = None,
            schedule_periods: Optional[int] = None,
            observers: Optional[Sequence[str]] = None,
            preferences: Optional[Mapping[str, SupportsStr]] = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.create_task(name, config_id, target_id, scanner_id, alterable=alterable,
                                   hosts_ordering=hosts_ordering, schedule_id=schedule_id, alert_ids=alert_ids,
                                   comment=comment, schedule_periods=schedule_periods, observers=observers,
                                   preferences=preferences)

    def update_task(
            self,
            task_id: Union[str, UUID],
            *,
            name: Optional[str] = None,
            config_id: Optional[Union[str, UUID]] = None,
            target_id: Optional[Union[str, UUID]] = None,
            scanner_id: Optional[Union[str, UUID]] = None,
            alterable: Optional[bool] = None,
            hosts_ordering: Optional[HostsOrdering] = None,
            schedule_id: Optional[Union[str, UUID]] = None,
            schedule_periods: Optional[int] = None,
            comment: Optional[str] = None,
            alert_ids: Optional[Sequence[Union[str, UUID]]] = None,
            observers: Optional[Sequence[str]] = None,
            preferences: Optional[Mapping[str, SupportsStr]] = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.modify_task(task_id, name=name, config_id=config_id, target_id=target_id, scanner_id=scanner_id,
                                   alterable=alterable, hosts_ordering=hosts_ordering, schedule_id=schedule_id,
                                   schedule_periods=schedule_periods, comment=comment, alert_ids=alert_ids,
                                   observers=observers, preferences=preferences)

    def delete_task(
            self,
            task_id: Union[str, UUID],
            *,
            ultimate: Optional[bool] = False
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.delete_task(task_id, ultimate=ultimate)

    def start_task(
            self,
            task_id: Union[str, UUID],
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.start_task(task_id)

    def resume_task(
            self,
            task_id: Union[str, UUID],
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.resume_task(task_id)

    def stop_task(
            self,
            task_id: Union[str, UUID],
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.stop_task(task_id)
