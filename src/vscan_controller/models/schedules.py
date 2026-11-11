from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from vscan_controller.models.base import BaseXmlGvmModel


class ScheduleTask(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: str | None = element(default=None)
    permissions: str | None = element(default=None)


class Schedule(BaseXmlGvmModel, search_mode="unordered", tag="schedule"):
    icalendar: str = element()
    timezone: str = element()
    tasks: list[ScheduleTask] | None = wrapped("tasks", element(tag="task"), default=None)


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
    comment: str | None = None


class ScheduleUpdate(BaseModel):
    name: str | None = None
    icalendar: str | None = None
    timezone: str | None = None
    comment: str | None = None
