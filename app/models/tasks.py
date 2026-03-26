from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Sequence
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
    trash: int = element()


class Target(BaseXmlModel, tag="target"):
    id: str = attr()
    name: str = element()
    trash: int = element()


class Scanner(BaseXmlModel, tag="scanner"):
    id: str = attr()
    name: str = element()
    type: int = element()
    trash: int = element()


class Schedule(BaseXmlModel, tag="schedule"):
    id: Optional[str] = attr()
    name: Optional[str] = element(default=None)
    trash: Optional[int] = element()


class ReportCount(BaseXmlModel, tag="report_count"):
    text: Optional[int]
    finished: str = element()


class Report(BaseXmlModel, tag="report"):
    id: str = attr()
    timestamp: datetime = element()
    scan_start: datetime = element(default=None)
    scan_end: datetime = element(default=None)


class Task(BaseXmlGvmModel, tag="task"):
    alterable: int = element()
    usage_type: str = element()
    config: Config = element()
    target: Target = element()
    scanner: Scanner = element()
    status: str = element()
    progress: int = element()
    report_count: ReportCount = element()
    trend: Optional[str] = element(default=None)
    schedule: Schedule = element()
    schedule_periods: int = element()
    current_report: Optional[Report] = wrapped("current_report", element(tag="report"), default=None)
    observers: Optional[str] = element(default=None)
    average_duration: Optional[int] = element(default=None)
    result_count: Optional[int] = element(default=None)
    preferences: List[Preference] = wrapped("preferences", element(tag="preference"))


# response and request models
class GetTasksResponse(BaseModel):
    tasks: List[Task]


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
