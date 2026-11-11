from datetime import datetime

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from vscan_controller.models.base import BaseXmlGvmModel


class ScannerCertificateInfo(BaseXmlModel, search_mode="unordered"):
    time_status: str = element()
    activation_time: datetime = element()
    expiration_time: datetime = element()
    issuer: str = element()
    md5_fingerprint: str = element()


class ScannerCredential(BaseXmlModel, search_mode="unordered", tag="credential"):
    id: str | None = attr()
    name: str | None = element(default=None)
    type: str | None = element(default=None)
    trash: bool | None = element()


class ScannerTask(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: str | None = element(default=None)
    permissions: str | None = element(default=None)


class ScannerConfig(BaseXmlModel, search_mode="unordered", tag="config"):
    id: str = attr()
    name: str | None = element(default=None)
    permissions: str | None = element(default=None)


class Scanner(BaseXmlGvmModel, search_mode="unordered", tag="scanner"):
    host: str | None = element(default=None)
    port: int | None = element()
    type: int | None = element()
    ca_pub_info: ScannerCertificateInfo | None = element(default=None, tag="ca_pub_info")
    certificate_info: ScannerCertificateInfo | None = element(default=None, tag="certificate_info")
    ca_pub: str | None = element(default=None)
    relay_host: str | None = element(default=None)
    relay_port: int | None = element()
    credential: ScannerCredential | None = element()
    configs: list[ScannerConfig] | None = wrapped("configs", element(tag="config", default=None))
    tasks: list[ScannerTask] | None = wrapped("tasks", element(tag="task"), default=None)


class GetScannerResponse(BaseModel):
    scanners: list[Scanner]
