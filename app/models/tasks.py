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


class TaskPreference(BaseXmlModel, search_mode="unordered", tag="preference"):
    name: str = element()
    scanner_name: str = element()
    value: str = element()


class TaskConfig(BaseXmlModel, search_mode="unordered", tag="config"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)
    trash: bool = element()


class TaskTarget(BaseXmlModel, search_mode="unordered", tag="target"):
    id: str = attr()
    name: str = element()
    permissions: Optional[str] = element(default=None)
    trash: bool = element()


class TaskScanner(BaseXmlModel, search_mode="unordered", tag="scanner"):
    id: str = attr()
    name: str = element()
    permissions: Optional[str] = element(default=None)
    type: int = element()
    trash: Optional[bool] = element(default=None)


class TaskSchedule(BaseXmlModel, search_mode="unordered", tag="schedule"):
    id: Optional[str] = attr()
    name: Optional[str] = element(default=None)
    icalendar: Optional[str] = element(default=None)
    timezone: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)
    trash: Optional[bool] = element()


class TaskReportResultCountElement(BaseXmlModel, search_mode="unordered"):
    count: int
    deprecated: Optional[bool] = attr(default=None)


class TaskReportResultCount(BaseXmlModel, search_mode="unordered"):
    log: TaskReportResultCountElement = element(tag="log")
    info: TaskReportResultCountElement = element(tag="info")
    low: TaskReportResultCountElement = element(tag="low")
    medium: TaskReportResultCountElement = element(tag="medium")
    warning: TaskReportResultCountElement = element(tag="warning")
    high: TaskReportResultCountElement = element(tag="high")
    critical: TaskReportResultCountElement = element(tag="critical")
    hole: TaskReportResultCountElement = element(tag="hole")
    false_positive: TaskReportResultCountElement = element(tag="false_positive")


class TaskReport(BaseXmlModel, search_mode="unordered", tag="report"):
    id: str = attr()
    timestamp: datetime = element()
    scan_start: datetime = element(default=None)
    scan_end: datetime = element(default=None)
    result_count: Optional[TaskReportResultCount] = element(tag="result_count", default=None)
    severity: Optional[float] = element(default=None)


class TaskReportCount(BaseXmlModel, search_mode="unordered", tag="report_count"):
    count: Optional[int]
    finished: int = element()


class TaskObserversGroup(BaseXmlModel, search_mode="unordered", tag="group"):
    id: str = attr()
    name: Optional[str] = element(default=None)


class TaskObserversRule(BaseXmlModel, search_mode="unordered", tag="rule"):
    id: str = attr()
    name: Optional[str] = element(default=None)


class TaskObservers(BaseXmlModel, search_mode="unordered", tag="observers"):
    user_list: Optional[str] = None
    groups: Optional[list[TaskObserversGroup]] = element(tag="group", default=None)
    rules: Optional[list[TaskObserversRule]] = element(tag="rule", default=None)


class Task(BaseXmlGvmModel, search_mode="unordered", tag="task"):
    alterable: bool = element()
    usage_type: str = element()
    config: TaskConfig = element()
    target: TaskTarget = element()
    hosts_ordering: Optional[str] = element(default=None)
    scanner: TaskScanner = element()
    status: str = element()
    progress: int = element()
    report_count: TaskReportCount = element()
    trend: Optional[str] = element(default=None)
    schedule: TaskSchedule = element()
    schedule_periods: int = element()
    current_report: Optional[TaskReport] = wrapped("current_report", element(default=None))
    last_report: Optional[TaskReport] = wrapped("last_report", element(default=None))
    observers: Optional[TaskObservers] = element(default=None)
    average_duration: Optional[int] = element(default=None)
    result_count: Optional[int] = element(default=None)
    preferences: list[TaskPreference] = wrapped("preferences", element(tag="preference"))


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
