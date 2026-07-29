from typing import Optional, Union

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from app.models.base import BaseXmlGvmModel


class PortList(BaseXmlModel, search_mode="unordered", tag="port_list"):
    id: str = attr()
    name: str = element()
    trash: bool = element()


class Credential(BaseXmlModel, search_mode="unordered"):
    id: Optional[str] = attr(default=None)
    name: Optional[str] = element(default=None)
    port: Optional[str] = element(default=None)
    trash: bool = element()


class AliveTests(BaseXmlModel, search_mode="unordered", tag="alive_tests"):
    text: Optional[str]
    alive_test: str = element()


class Task(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: Optional[str] = element(default=None)
    permissions: Optional[str] = element(default=None)


class Target(BaseXmlGvmModel, tag="target"):
    hosts: list[str] = element()
    exclude_hosts: Optional[list[str]] = element(default=None)
    max_hosts: int = element()
    port_list: PortList = element()
    port_range: Optional[str] = element(default=None)
    ssh_credential: Credential = element()
    smb_credential: Credential = element()
    esxi_credential: Credential = element()
    snmp_credential: Credential = element()
    ssh_elevate_credential: Credential = element()
    krb5_credential: Credential = element()
    reverse_lookup_only: bool = element()
    reverse_lookup_unify: bool = element()
    allow_simultaneous_ips: bool = element()
    alive_tests: AliveTests = element()
    tasks: Optional[list[Task]] = wrapped("tasks", element(tag="task"), default=None)


# response and request models
class GetTargetsResponse(BaseModel):
    targets: list[Target]


class GetTargetResponse(BaseModel):
    target: Target


class CreateTargetResponse(BaseModel):
    id: str


class TargetCreate(BaseModel):
    name: str
    asset_hosts_filter: Optional[str] = None
    hosts: Optional[list[str]] = None
    comment: Optional[str] = None
    exclude_hosts: Optional[list[str]] = None
    ssh_credential_id: Optional[str] = None
    ssh_credential_port: Optional[Union[int, str]] = None
    smb_credential_id: Optional[str] = None
    esxi_credential_id: Optional[str] = None
    snmp_credential_id: Optional[str] = None
    alive_test: Optional[str] = None
    allow_simultaneous_ips: Optional[bool] = None
    reverse_lookup_only: Optional[bool] = None
    reverse_lookup_unify: Optional[bool] = None
    port_range: Optional[str] = None
    port_list_id: Optional[str] = None


class TargetUpdate(BaseModel):
    name: Optional[str] = None
    comment: Optional[str] = None
    hosts: Optional[list[str]] = None
    exclude_hosts: Optional[list[str]] = None
    ssh_credential_id: Optional[str] = None
    ssh_credential_port: Optional[Union[str, int]] = None
    smb_credential_id: Optional[str] = None
    esxi_credential_id: Optional[str] = None
    snmp_credential_id: Optional[str] = None
    alive_test: Optional[str] = None
    allow_simultaneous_ips: Optional[bool] = None
    reverse_lookup_only: Optional[bool] = None
    reverse_lookup_unify: Optional[bool] = None
    port_list_id: Optional[str] = None
