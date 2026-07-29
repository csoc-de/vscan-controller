from typing import Optional

from pydantic import BaseModel
from pydantic_xml import element, attr, BaseXmlModel, wrapped

from app.models.base import BaseXmlGvmModel


class ConfigScanner(BaseXmlModel, search_mode="unordered", tag="scanner"):
    id: str = attr()
    trash: bool = element()


class ConfigCount(BaseXmlModel, search_mode="unordered"):
    value: int
    growing: Optional[bool] = element(default=None)


class ConfigTask(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class ConfigFamily(BaseXmlModel, search_mode="unordered", tag="family"):
    name: str = element()
    nvt_count: int = element()
    max_nvt_count: int = element()
    growing: Optional[bool] = element(default=None)


class ConfigPreferenceNVT(BaseXmlModel, search_mode="unordered", tag="nvt"):
    oid: str = attr()
    name: str = element()


class ConfigPreference(BaseXmlModel, search_mode="unordered", tag="preference"):
    nvt: ConfigPreferenceNVT = element()
    name: str = element()
    id: str = element()
    type: str = element()
    value: str = element()
    default: str = element()
    alts: list[str] = element(tag="alt")


class ConfigNVTSelector(BaseXmlModel, search_mode="unordered", tag="nvt_selector"):
    name: str = element()
    include: bool = element()
    type: str = element()
    family_or_nvt: str = element()


class Config(BaseXmlGvmModel, search_mode="unordered", tag="config"):
    max_nvt_count: Optional[int] = element(default=None)
    known_nvt_count: Optional[int] = element(default=None)
    scanner: Optional[ConfigScanner] = element(default=None)
    family_count: ConfigCount = element()
    nvt_count: ConfigCount = element()
    type: int = element()
    usage_type: str = element()
    predefined: bool = element()
    tasks: Optional[list[ConfigTask]] = wrapped("tasks", element(tag="task"), default=None)
    families: Optional[list[ConfigFamily]] = wrapped("families", element(tag="family"), default=None)
    preferences: Optional[list[ConfigPreference]] = wrapped("preferences", element(tag="preference"), default=None)
    nvt_selectors: Optional[ConfigNVTSelector] = wrapped("nvt_selectors", element(tag="nvt_selector"), default=None)
    deprecated: Optional[bool] = element(default=None)


class GetConfigsResponse(BaseModel):
    configs: list[Config]
