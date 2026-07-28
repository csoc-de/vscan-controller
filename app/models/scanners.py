from typing import Optional

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, element, attr, wrapped

from app.models.base import BaseXmlGvmModel, CertificateInfo


class Credential(BaseXmlModel, search_mode='unordered', tag="credential"):
    id: Optional[str] = attr()
    name: Optional[str] = element(default=None)
    type: Optional[str] = element(default=None)
    trash: Optional[bool] = element()


class Task(BaseXmlModel, search_mode='unordered', tag="task"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class Config(BaseXmlModel, search_mode='unordered', tag="config"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class Scanner(BaseXmlGvmModel, tag="scanner"):
    host: Optional[str] = element(default=None)
    port: Optional[int] = element()
    type: Optional[int] = element()
    ca_pub_info: Optional[CertificateInfo] = element(default=None, tag="ca_pub_info")
    certificate_info: Optional[CertificateInfo] = element(default=None, tag="certificate_info")
    ca_pub: Optional[str] = element(default=None)
    relay_host: Optional[str] = element(default=None)
    relay_port: Optional[int] = element()
    credentials: Optional[Credential] = element()
    configs: Optional[list[Config]] = wrapped("configs", element(tag="config", default=None))
    tasks: Optional[list[Task]] = wrapped("tasks", element(tag="task"), default=None)


class GetScannerResponse(BaseModel):
    scanners: list[Scanner]
