from datetime import datetime
from enum import Enum
from typing import Optional, Union, Sequence
from uuid import UUID

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from app.models.base import BaseXmlGvmModel


class HostsOrdering(Enum):
    """Enum for host ordering during scans"""

    SEQUENTIAL = "sequential"
    RANDOM = "random"
    REVERSE = "reverse"


class Preference(BaseXmlModel, tag="preference"):
    name: str = element()
    scanner_name: str = element()
    value: str = element()


class Config(BaseXmlModel, tag="config"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)
    trash: bool = element()


class Target(BaseXmlModel, tag="target"):
    id: str = attr()
    name: str = element()
    permissions: Optional[str] = element(default=None)
    trash: bool = element()


class Scanner(BaseXmlModel, tag="scanner"):
    id: str = attr()
    name: str = element()
    permissions: Optional[str] = element(default=None)
    type: int = element()
    trash: bool = element(default=False)


class Schedule(BaseXmlModel, tag="schedule"):
    id: Optional[str] = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)
    trash: Optional[int] = element()


class ReportCount(BaseXmlModel, tag="report_count"):
    text: Optional[int]
    finished: str = element()


class Report(BaseXmlModel, tag="report"):
    id: str = attr()
    timestamp: datetime = element()
    scan_start: datetime = element(default=None)
    scan_end: datetime = element(default=None)
    result_count: Optional[ResultCount] = element(tag="result_count", default=None)
    severity: Optional[float] = element(default=None)


class ObserverGroup(BaseXmlModel, tag="group"):
    id: str = attr()
    name: Optional[str] = element(default=None)


class ObserverRule(BaseXmlModel, tag="rule"):
    id: str = attr()
    name: Optional[str] = element(default=None)


class Observers(BaseXmlModel, tag="observers"):
    groups: Optional[list[ObserverGroup]] = element(tag="group", default=None)
    rules: Optional[list[ObserverRule]] = element(tag="rule", default=None)


class Task(BaseXmlGvmModel, tag="task"):
    alterable: int = element()
    usage_type: str = element()
    config: Config = element()
    target: Target = element()
    hosts_ordering: Optional[str] = element(default=None)
    scanner: Scanner = element()
    status: str = element()
    progress: int = element()
    report_count: ReportCount = element()
    trend: Optional[str] = element(default=None)
    schedule: Schedule = element()
    schedule_periods: int = element()
    current_report: Optional[Report] = wrapped("current_report", element(default=None))
    last_report: Optional[Report] = wrapped("last_report", element(default=None))
    observers: Optional[list[Observers]] = element(default=None)
    average_duration: Optional[int] = element(default=None)
    result_count: Optional[int] = element(default=None)
    preferences: list[Preference] = wrapped("preferences", element(tag="preference"))


# response and request models
class GetTasksResponse(BaseModel):
    tasks: list[Task]


class GetTaskResponse(BaseModel):
    task: Task


class CreateTaskResponse(BaseModel):
    id: str


class TaskCreate(BaseModel):
    name: str
    config_id: Union[str, UUID]
    target_id: Union[str, UUID]
    scanner_id: Union[str, UUID]
    alterable: Optional[bool] = None
    hosts_ordering: Optional[HostsOrdering] = None
    schedule_id: Optional[Union[str, UUID]] = None
    alert_ids: Optional[Sequence[Union[str, UUID]]] = None
    comment: Optional[str] = None
    schedule_periods: Optional[int] = None
    observers: Optional[Sequence[str]] = None
    preferences: Optional[str] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    config_id: Optional[Union[str, UUID]] = None
    target_id: Optional[Union[str, UUID]] = None
    scanner_id: Optional[Union[str, UUID]] = None
    alterable: Optional[bool] = None
    hosts_ordering: Optional[HostsOrdering] = None
    schedule_id: Optional[Union[str, UUID]] = None
    schedule_periods: Optional[int] = None
    comment: Optional[str] = None
    alert_ids: Optional[Sequence[Union[str, UUID]]] = None
    observers: Optional[Sequence[str]] = None
    preferences: Optional[str] = None
