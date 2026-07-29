from typing import Optional

from pydantic import BaseModel
from pydantic_xml import element, attr, wrapped, BaseXmlModel

from app.models.base import BaseXmlGvmModel


class Task(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class Schedule(BaseXmlGvmModel, tag="schedule"):
    icalendar: str = element()
    timezone: str = element()
    tasks: Optional[list[Task]] = wrapped("tasks", element(tag="task"), default=None)


# response and request models
class GetSchedulesResponse(BaseModel):
    schedules: list[Schedule]


class GetScheduleResponse(BaseModel):
    schedule: Schedule


class CreateScheduleResponse(BaseModel):
    id: str


class ScheduleCreate(BaseModel):
    name: str
    icalendar: str
    timezone: str
    comment: Optional[str] = None


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    icalendar: Optional[str] = None
    timezone: Optional[str] = None
    comment: Optional[str] = None
