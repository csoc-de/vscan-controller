from typing import Optional

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, element, attr, wrapped

from app.models.base import BaseXmlGvmModel


class PortListPortCount(BaseXmlModel, search_mode="unordered", tag="port_count"):
    all: int = element()
    tcp: int = element()
    udp: int = element()


class PortListPortRange(BaseXmlModel, search_mode="unordered", tag="port_range"):
    id: str = attr()
    start: str = element()
    end: str = element()
    type: str = element()
    comment: str = element()


class PortListTarget(BaseXmlModel, search_mode="unordered", tag="target"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class PortList(BaseXmlGvmModel, search_mode="unordered", tag="port_list"):
    port_count: PortListPortCount = element()
    predefined: bool = element()
    port_ranges: Optional[list[PortListPortRange]] = wrapped("port_ranges", element(tag="port_range"), default=None)
    targets: Optional[list[PortListTarget]] = wrapped("targets", element(tag="target"), default=None)
    deprecated: Optional[bool] = element(default=None)


class GetPortListsResponse(BaseModel):
    port_lists: list[PortList]
