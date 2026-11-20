from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from vscan_controller.models.base import BaseXmlGvmModel


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
    name: str | None = element(default=None)
    permissions: str | None = element(default=None)


class PortList(BaseXmlGvmModel, search_mode="unordered", tag="port_list"):
    port_count: PortListPortCount = element()
    predefined: bool = element()
    port_ranges: list[PortListPortRange] | None = wrapped(
        "port_ranges", element(tag="port_range"), default=None
    )
    targets: list[PortListTarget] | None = wrapped("targets", element(tag="target"), default=None)
    deprecated: bool | None = element(default=None)


class GetPortListsResponse(BaseModel):
    port_lists: list[PortList]
