from typing import List, Optional

from pydantic import BaseModel
from pydantic_xml import element

from app.models.base import BaseXmlGvmModel


class Schedule(BaseXmlGvmModel, tag="schedule"):
    icalendar: str = element()
    timezone: str = element()


# response and request models
class GetSchedulesResponse(BaseModel):
    schedules: List[Schedule]


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
