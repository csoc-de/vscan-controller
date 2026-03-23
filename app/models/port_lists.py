from datetime import datetime
from typing import List

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, element, wrapped


class Owner(BaseXmlModel, tag="owner"):
    name: str = element()


class PortCount(BaseXmlModel, tag="port_count"):
    all: int = element()
    tcp: int = element()
    udp: int = element()


class Permission(BaseXmlModel, tag="permission"):
    name: str = element()


class PortList(BaseXmlModel, tag="port_list"):
    id: str = attr(name="id")
    owner: Owner = element()
    name: str = element()
    comment: str = element()
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: int = element()
    in_use: int = element()
    permissions: List[Permission] = wrapped("permissions", element())
    port_count: PortCount = element()
    predefined: int = element()


class GetPortListsResponse(BaseModel):
    port_lists: List[PortList]
