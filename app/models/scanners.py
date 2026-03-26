from typing import List, Optional

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, element, attr

from app.models.base import BaseXmlGvmModel


class Credential(BaseXmlModel, tag="credential"):
    id: Optional[str] = attr()
    name: Optional[str] = element(default=None)
    type: Optional[str] = element(default=None)
    trash: Optional[int] = element()


class Scanner(BaseXmlGvmModel, tag="scanner"):
    host: Optional[str] = element(default=None)
    port: Optional[int] = element()
    type: Optional[int] = element()
    ca_pub: Optional[str] = element(default=None)
    relay_host: Optional[str] = element(default=None)
    relay_port: Optional[int] = element()
    credentials: Optional[Credential] = element()


class GetScannerResponse(BaseModel):
    scanners: List[Scanner]
