from typing import Optional

from pydantic import BaseModel
from pydantic_xml import element, attr, BaseXmlModel, wrapped

from app.models.base import BaseXmlGvmModel


class Scanner(BaseXmlModel, search_mode="unordered", tag="scanner"):
    id: str = attr()
    trash: bool = element()


class Count(BaseXmlModel, search_mode="unordered"):
    text: int
    growing: Optional[bool] = element(default=None)


class Task(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class Family(BaseXmlModel, search_mode="unordered", tag="family"):
    name: str = element()
    nvt_count: int = element()
    max_nvt_count: int = element()
    growing: Optional[bool] = element(default=None)


class PreferenceNVT(BaseXmlModel, search_mode="unordered", tag="nvt"):
    oid: str = attr()
    name: str = element()


class Preference(BaseXmlModel, search_mode="unordered", tag="preference"):
    nvt: PreferenceNVT = element()
    name: str = element()
    id: str = element()
    type: str = element()
    value: str = element()
    default: str = element()
    alts: list[str] = element(tag="alt")


class NVTSelector(BaseXmlModel, search_mode="unordered", tag="nvt_selector"):
    name: str = element()
    include: bool = element()
    type: str = element()
    family_or_nvt: str = element()


class Config(BaseXmlGvmModel, search_mode="unordered", tag="config"):
    max_nvt_count: Optional[int] = element(default=None)
    known_nvt_count: Optional[int] = element(default=None)
    scanner: Optional[Scanner] = element(default=None)
    family_count: Count = element()
    nvt_count: Count = element()
    type: int = element()
    usage_type: str = element()
    predefined: bool = element()
    tasks: Optional[list[Task]] = wrapped("tasks", element(tag="task"), default=None)
    families: Optional[list[Task]] = wrapped("families", element(tag="family"), default=None)
    preferences: Optional[list[Preference]] = wrapped("preferences", element(tag="preference"), default=None)
    nvt_selectors: Optional[NVTSelector] = wrapped("nvt_selectors", element(tag="nvt_selector"), default=None)
    deprecated: Optional[bool] = element(default=None)


class GetConfigsResponse(BaseModel):
    configs: list[Config]
