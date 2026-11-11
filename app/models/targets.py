from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from app.models.base import BaseXmlGvmModel


class TargetPortList(BaseXmlModel, search_mode="unordered", tag="port_list"):
    id: str = attr()
    name: str = element()
    trash: bool = element()


class TargetCredential(BaseXmlModel, search_mode="unordered"):
    id: str | None = attr(default=None)
    name: str | None = element(default=None)
    port: str | None = element(default=None)
    trash: bool = element()


class TargetAliveTests(BaseXmlModel, search_mode="unordered", tag="alive_tests"):
    text: str | None
    alive_test: str = element()


class TargetTask(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: str | None = element(default=None)
    permissions: str | None = element(default=None)


class Target(BaseXmlGvmModel, search_mode="unordered", tag="target"):
    hosts: list[str] = element()
    exclude_hosts: list[str] | None = element(default=None)
    max_hosts: int = element()
    port_list: TargetPortList = element()
    port_range: str | None = element(default=None)
    ssh_credential: TargetCredential = element()
    smb_credential: TargetCredential = element()
    esxi_credential: TargetCredential = element()
    snmp_credential: TargetCredential = element()
    ssh_elevate_credential: TargetCredential = element()
    krb5_credential: TargetCredential = element()
    reverse_lookup_only: bool = element()
    reverse_lookup_unify: bool = element()
    allow_simultaneous_ips: bool = element()
    alive_tests: TargetAliveTests = element()
    tasks: list[TargetTask] | None = wrapped("tasks", element(tag="task"), default=None)


# response and request models
class GetTargetsResponse(BaseModel):
    targets: list[Target]


class GetTargetResponse(BaseModel):
    target: Target


class CreateTargetResponse(BaseModel):
    id: str


class TargetCreate(BaseModel):
    name: str
    asset_hosts_filter: str | None = None
    hosts: list[str] | None = None
    comment: str | None = None
    exclude_hosts: list[str] | None = None
    ssh_credential_id: str | None = None
    ssh_credential_port: int | str | None = None
    smb_credential_id: str | None = None
    esxi_credential_id: str | None = None
    snmp_credential_id: str | None = None
    alive_test: str | None = None
    allow_simultaneous_ips: bool | None = None
    reverse_lookup_only: bool | None = None
    reverse_lookup_unify: bool | None = None
    port_range: str | None = None
    port_list_id: str | None = None


class TargetUpdate(BaseModel):
    name: str | None = None
    comment: str | None = None
    hosts: list[str] | None = None
    exclude_hosts: list[str] | None = None
    ssh_credential_id: str | None = None
    ssh_credential_port: str | int | None = None
    smb_credential_id: str | None = None
    esxi_credential_id: str | None = None
    snmp_credential_id: str | None = None
    alive_test: str | None = None
    allow_simultaneous_ips: bool | None = None
    reverse_lookup_only: bool | None = None
    reverse_lookup_unify: bool | None = None
    port_list_id: str | None = None
