from typing import List

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, element

from app.models.base import BaseXmlGvmModel


class PortCount(BaseXmlModel, tag="port_count"):
    all: int = element()
    tcp: int = element()
    udp: int = element()


class PortList(BaseXmlGvmModel, tag="port_list"):
    port_count: PortCount = element()
    predefined: int = element()


class GetPortListsResponse(BaseModel):
    port_lists: List[PortList]
