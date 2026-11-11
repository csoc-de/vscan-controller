import os
from datetime import UTC, datetime

from vscan_controller.models.scanners import Scanner


def test_scanner_parsing_xml_to_model():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "scanner.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    scanner = Scanner.from_xml(xml_content)

    # --- Top-Level ---
    assert scanner.id == "08b69003-5fc2-4037-a479-93b440211c73"
    assert scanner.owner.name is None
    assert scanner.name == "OpenVAS Default"
    assert scanner.comment is None
    assert scanner.creation_time == datetime(2026, 4, 24, 12, 36, 46, tzinfo=UTC)
    assert scanner.modification_time == datetime(2026, 4, 24, 12, 36, 46, tzinfo=UTC)
    assert scanner.writable is True
    assert scanner.in_use is True
    assert scanner.ca_pub is None
    assert scanner.relay_host is None
    assert scanner.relay_port == 0
    assert scanner.host == "/run/ospd/ospd-openvas.sock"
    assert scanner.port == 0
    assert scanner.type == 2

    # --- Permissions ---
    assert len(scanner.permissions) == 4
    assert scanner.permissions[0].name == "get_scanners"
    assert scanner.permissions[1].name == "get_scanners"
    assert scanner.permissions[2].name == "get_scanners"
    assert scanner.permissions[3].name == "get_scanners"

    # --- Credential ---
    assert scanner.credential.id == ""
    assert scanner.credential.name is None
    assert scanner.credential.type is None
    assert scanner.credential.trash is False
