from collections.abc import Sequence
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from vscan_controller.models.base import BaseXmlGvmModel


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
    name: str | None = element(default=None)
    permissions: str | None = element(default=None)
    trash: bool = element()


class TaskTarget(BaseXmlModel, search_mode="unordered", tag="target"):
    id: str = attr()
    name: str = element()
    permissions: str | None = element(default=None)
    trash: bool = element()


class TaskScanner(BaseXmlModel, search_mode="unordered", tag="scanner"):
    id: str = attr()
    name: str = element()
    permissions: str | None = element(default=None)
    type: int = element()
    trash: bool | None = element(default=None)


class TaskSchedule(BaseXmlModel, search_mode="unordered", tag="schedule"):
    id: str | None = attr()
    name: str | None = element(default=None)
    icalendar: str | None = element(default=None)
    timezone: str | None = element(default=None)
    permissions: str | None = element(default=None)
    trash: bool | None = element()


class TaskReportResultCountElement(BaseXmlModel, search_mode="unordered"):
    count: int
    deprecated: bool | None = attr(default=None)


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
    result_count: TaskReportResultCount | None = element(tag="result_count", default=None)
    severity: float | None = element(default=None)


class TaskReportCount(BaseXmlModel, search_mode="unordered", tag="report_count"):
    count: int | None
    finished: int = element()


class TaskObserversGroup(BaseXmlModel, search_mode="unordered", tag="group"):
    id: str = attr()
    name: str | None = element(default=None)


class TaskObserversRule(BaseXmlModel, search_mode="unordered", tag="rule"):
    id: str = attr()
    name: str | None = element(default=None)


class TaskObservers(BaseXmlModel, search_mode="unordered", tag="observers"):
    user_list: str | None = None
    groups: list[TaskObserversGroup] | None = element(tag="group", default=None)
    rules: list[TaskObserversRule] | None = element(tag="rule", default=None)


class Task(BaseXmlGvmModel, search_mode="unordered", tag="task"):
    alterable: bool = element()
    usage_type: str = element()
    config: TaskConfig = element()
    target: TaskTarget = element()
    hosts_ordering: str | None = element(default=None)
    scanner: TaskScanner = element()
    status: str = element()
    progress: int = element()
    report_count: TaskReportCount = element()
    trend: str | None = element(default=None)
    schedule: TaskSchedule = element()
    schedule_periods: int = element()
    current_report: TaskReport | None = wrapped("current_report", element(default=None))
    last_report: TaskReport | None = wrapped("last_report", element(default=None))
    observers: TaskObservers | None = element(default=None)
    average_duration: int | None = element(default=None)
    result_count: int | None = element(default=None)
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
    config_id: str | UUID
    target_id: str | UUID
    scanner_id: str | UUID
    alterable: bool | None = None
    hosts_ordering: HostsOrdering | None = None
    schedule_id: str | UUID | None = None
    alert_ids: Sequence[str | UUID] | None = None
    comment: str | None = None
    schedule_periods: int | None = None
    observers: Sequence[str] | None = None
    preferences: str | None = None


class TaskUpdate(BaseModel):
    name: str | None = None
    config_id: str | UUID | None = None
    target_id: str | UUID | None = None
    scanner_id: str | UUID | None = None
    alterable: bool | None = None
    hosts_ordering: HostsOrdering | None = None
    schedule_id: str | UUID | None = None
    schedule_periods: int | None = None
    comment: str | None = None
    alert_ids: Sequence[str | UUID] | None = None
    observers: Sequence[str] | None = None
    preferences: str | None = None
