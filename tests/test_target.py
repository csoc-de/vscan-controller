import os
from datetime import UTC, datetime

from app.models.targets import Target


def test_target_parsing_xml_to_model():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "target.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    target = Target.from_xml(xml_content)

    # --- Top-Level ---
    assert target.id == "70465d32-2f65-4c34-944b-2e8b10432aee"
    assert target.owner.name == "admin"
    assert target.name == "Target:HOME without Gast network:dc4f38be-bd66-4d68-b5f8-ff5cec315cbf"
    assert target.comment == "It scan my home network without gast network"
    assert target.creation_time == datetime(2026, 7, 20, 10, 12, 9, tzinfo=UTC)
    assert target.modification_time == datetime(2026, 7, 20, 10, 12, 9, tzinfo=UTC)
    assert target.writable is True
    assert target.in_use is True
    assert target.hosts == ["192.168.0.101"]
    assert target.exclude_hosts == ["192.168.100.0-192.168.100.75"]
    assert target.max_hosts == 1
    assert target.reverse_lookup_only is False
    assert target.reverse_lookup_unify is False
    assert target.allow_simultaneous_ips is True

    # --- Permissions ---
    assert len(target.permissions) == 1
    assert target.permissions[0].name == "Everything"

    # --- Port List ---
    assert target.port_list.id == "33d0cd82-57c6-11e1-8ed1-406186ea4fc5"
    assert target.port_list.name == "All IANA assigned TCP"
    assert target.port_list.trash is False

    # --- Credentials ---
    # SSH
    assert target.ssh_credential.id == ""
    assert target.ssh_credential.name is None
    assert target.ssh_credential.port is None
    assert target.ssh_credential.trash is False

    # SMB
    assert target.smb_credential.id == ""
    assert target.smb_credential.name is None
    assert target.smb_credential.trash is False

    # ESXi
    assert target.esxi_credential.id == ""
    assert target.esxi_credential.name is None
    assert target.esxi_credential.trash is False

    # SNMP
    assert target.snmp_credential.id == ""
    assert target.snmp_credential.name is None
    assert target.snmp_credential.trash is False

    # SSH Elevate
    assert target.ssh_elevate_credential.id == ""
    assert target.ssh_elevate_credential.name is None
    assert target.ssh_elevate_credential.trash is False

    # Kerberos
    assert target.krb5_credential.id == ""
    assert target.krb5_credential.name is None
    assert target.krb5_credential.trash is False

    # --- Alive Tests ---
    assert target.alive_tests.text == "Scan Config Default"
    assert target.alive_tests.alive_test == "Scan Config Default"
