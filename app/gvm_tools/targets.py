from typing import Any, Optional, Union
from uuid import UUID

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform


class GVMTargets:
    def __init__(self, socket: UnixSocketConnection, transform: EtreeCheckCommandTransform, user: str,
                 password: str) -> None:
        self.socket = socket
        self.transform = transform
        self.user: str = user
        self.password: str = password

    def get_target(self, target_id: str) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_target(target_id)

    def get_targets(self, filter_str: str = None, trash: bool = False) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_targets(filter_string=filter_str, trash=trash)

    def create_target(
            self,
            name: str,
            *,
            asset_hosts_filter: Optional[str] = None,
            hosts: Optional[list[str]] = None,
            comment: Optional[str] = None,
            exclude_hosts: Optional[list[str]] = None,
            ssh_credential_id: Optional[Union[str, UUID]] = None,
            ssh_credential_port: Optional[Union[int, str]] = None,
            smb_credential_id: Optional[Union[str, UUID]] = None,
            esxi_credential_id: Optional[Union[str, UUID]] = None,
            snmp_credential_id: Optional[Union[str, UUID]] = None,
            alive_test: Optional[str] = None,
            allow_simultaneous_ips: Optional[bool] = None,
            reverse_lookup_only: Optional[bool] = None,
            reverse_lookup_unify: Optional[bool] = None,
            port_range: Optional[str] = None,
            port_list_id: Optional[Union[str, UUID]] = None
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.create_target(name, asset_hosts_filter=asset_hosts_filter, hosts=hosts, comment=comment,
                                     exclude_hosts=exclude_hosts, ssh_credential_id=ssh_credential_id,
                                     ssh_credential_port=ssh_credential_port, smb_credential_id=smb_credential_id,
                                     esxi_credential_id=esxi_credential_id, snmp_credential_id=snmp_credential_id,
                                     alive_test=alive_test, allow_simultaneous_ips=allow_simultaneous_ips,
                                     reverse_lookup_only=reverse_lookup_only, reverse_lookup_unify=reverse_lookup_unify,
                                     port_range=port_range, port_list_id=port_list_id)

    def update_target(
            self,
            target_id: Union[str, UUID],
            *,
            name: Optional[str] = None,
            comment: Optional[str] = None,
            hosts: Optional[list[str]] = None,
            exclude_hosts: Optional[list[str]] = None,
            ssh_credential_id: Optional[Union[str, UUID]] = None,
            ssh_credential_port: Optional[Union[str, int]] = None,
            smb_credential_id: Optional[Union[str, UUID]] = None,
            esxi_credential_id: Optional[Union[str, UUID]] = None,
            snmp_credential_id: Optional[Union[str, UUID]] = None,
            alive_test: Optional[str] = None,
            allow_simultaneous_ips: Optional[bool] = None,
            reverse_lookup_only: Optional[bool] = None,
            reverse_lookup_unify: Optional[bool] = None,
            port_list_id: Optional[Union[str, UUID]] = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.modify_target(target_id, name=name, comment=comment, hosts=hosts, exclude_hosts=exclude_hosts,
                                     ssh_credential_id=ssh_credential_id, ssh_credential_port=ssh_credential_port,
                                     smb_credential_id=smb_credential_id, esxi_credential_id=esxi_credential_id,
                                     snmp_credential_id=snmp_credential_id, alive_test=alive_test,
                                     allow_simultaneous_ips=allow_simultaneous_ips,
                                     reverse_lookup_only=reverse_lookup_only, reverse_lookup_unify=reverse_lookup_unify,
                                     port_list_id=port_list_id)

    def delete_target(
            self,
            target_id: Union[str, UUID],
            *,
            ultimate: Optional[bool] = False
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.delete_target(target_id, ultimate=ultimate)
