from typing import Optional

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, element, attr, wrapped

from app.models.base import BaseXmlGvmModel


class PortCount(BaseXmlModel, tag="port_count"):
    all: int = element()
    tcp: int = element()
    udp: int = element()


class PortRange(BaseXmlModel, tag="port_range"):
    id: str = attr()
    start: str = element()
    end: str = element()
    type: str = element()
    comment: str = element()


class Target(BaseXmlModel, tag="target"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class PortList(BaseXmlGvmModel, tag="port_list"):
    port_count: PortCount = element()
    predefined: bool = element()
    port_ranges: Optional[list[PortRange]] = wrapped("port_ranges", element(tag="port_range"), default=None)
    targets: Optional[list[Target]] = wrapped("targets", element(tag="target"), default=None)
    deprecated: Optional[bool] = element(default=None)


class GetPortListsResponse(BaseModel):
    port_lists: list[PortList]
