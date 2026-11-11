from typing import Any
from uuid import UUID

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform


class GVMTargets:
    def __init__(
        self,
        socket: UnixSocketConnection,
        transform: EtreeCheckCommandTransform,
        user: str,
        password: str,
    ) -> None:
        self.socket = socket
        self.transform = transform
        self.user: str = user
        self.password: str = password

    def get_target(self, target_id: str) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_target(target_id)

    def get_targets(self, filter_string: str | None = None, trash: bool | None = False) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.get_targets(filter_string=filter_string, trash=trash)

    def create_target(
        self,
        name: str,
        *,
        asset_hosts_filter: str | None = None,
        hosts: list[str] | None = None,
        comment: str | None = None,
        exclude_hosts: list[str] | None = None,
        ssh_credential_id: str | UUID | None = None,
        ssh_credential_port: int | str | None = None,
        smb_credential_id: str | UUID | None = None,
        esxi_credential_id: str | UUID | None = None,
        snmp_credential_id: str | UUID | None = None,
        alive_test: str | None = None,
        allow_simultaneous_ips: bool | None = None,
        reverse_lookup_only: bool | None = None,
        reverse_lookup_unify: bool | None = None,
        port_range: str | None = None,
        port_list_id: str | UUID | None = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.create_target(
                name,
                asset_hosts_filter=asset_hosts_filter,
                hosts=hosts,
                comment=comment,
                exclude_hosts=exclude_hosts,
                ssh_credential_id=ssh_credential_id,
                ssh_credential_port=ssh_credential_port,
                smb_credential_id=smb_credential_id,
                esxi_credential_id=esxi_credential_id,
                snmp_credential_id=snmp_credential_id,
                alive_test=alive_test,
                allow_simultaneous_ips=allow_simultaneous_ips,
                reverse_lookup_only=reverse_lookup_only,
                reverse_lookup_unify=reverse_lookup_unify,
                port_range=port_range,
                port_list_id=port_list_id,
            )

    def update_target(
        self,
        target_id: str | UUID,
        *,
        name: str | None = None,
        comment: str | None = None,
        hosts: list[str] | None = None,
        exclude_hosts: list[str] | None = None,
        ssh_credential_id: str | UUID | None = None,
        ssh_credential_port: str | int | None = None,
        smb_credential_id: str | UUID | None = None,
        esxi_credential_id: str | UUID | None = None,
        snmp_credential_id: str | UUID | None = None,
        alive_test: str | None = None,
        allow_simultaneous_ips: bool | None = None,
        reverse_lookup_only: bool | None = None,
        reverse_lookup_unify: bool | None = None,
        port_list_id: str | UUID | None = None,
    ) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.modify_target(
                target_id,
                name=name,
                comment=comment,
                hosts=hosts,
                exclude_hosts=exclude_hosts,
                ssh_credential_id=ssh_credential_id,
                ssh_credential_port=ssh_credential_port,
                smb_credential_id=smb_credential_id,
                esxi_credential_id=esxi_credential_id,
                snmp_credential_id=snmp_credential_id,
                alive_test=alive_test,
                allow_simultaneous_ips=allow_simultaneous_ips,
                reverse_lookup_only=reverse_lookup_only,
                reverse_lookup_unify=reverse_lookup_unify,
                port_list_id=port_list_id,
            )

    def delete_target(self, target_id: str | UUID, *, ultimate: bool | None = False) -> Any:
        with GMP(connection=self.socket, transform=self.transform) as gvm:
            gvm.authenticate(self.user, self.password)
            return gvm.delete_target(target_id, ultimate=ultimate)
