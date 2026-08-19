from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, element, attr, wrapped

from app.models.base import BaseXmlGvmModel


class ScannerCertificateInfo(BaseXmlModel, search_mode="unordered"):
    time_status: str = element()
    activation_time: datetime = element()
    expiration_time: datetime = element()
    issuer: str = element()
    md5_fingerprint: str = element()


class ScannerCredential(BaseXmlModel, search_mode="unordered", tag="credential"):
    id: Optional[str] = attr()
    name: Optional[str] = element(default=None)
    type: Optional[str] = element(default=None)
    trash: Optional[bool] = element()


class ScannerTask(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class ScannerConfig(BaseXmlModel, search_mode="unordered", tag="config"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class Scanner(BaseXmlGvmModel, search_mode="unordered", tag="scanner"):
    host: Optional[str] = element(default=None)
    port: Optional[int] = element()
    type: Optional[int] = element()
    ca_pub_info: Optional[ScannerCertificateInfo] = element(default=None, tag="ca_pub_info")
    certificate_info: Optional[ScannerCertificateInfo] = element(default=None, tag="certificate_info")
    ca_pub: Optional[str] = element(default=None)
    relay_host: Optional[str] = element(default=None)
    relay_port: Optional[int] = element()
    credential: Optional[ScannerCredential] = element()
    configs: Optional[list[ScannerConfig]] = wrapped("configs", element(tag="config", default=None))
    tasks: Optional[list[ScannerTask]] = wrapped("tasks", element(tag="task"), default=None)


class GetScannerResponse(BaseModel):
    scanners: list[Scanner]
