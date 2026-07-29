import os
from datetime import datetime, timezone

from app.models.port_lists import PortList


def test_port_list_parsing_xml_to_model():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "port_list.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    port_list = PortList.from_xml(xml_content)

    # --- Top-Level ---
    assert port_list.id == "33d0cd82-57c6-11e1-8ed1-406186ea4fc5"
    assert port_list.owner.name == "admin"
    assert port_list.name == "All IANA assigned TCP"
    assert port_list.comment == "Version 20200827."
    assert port_list.creation_time == datetime(2026, 4, 24, 12, 36, 48, tzinfo=timezone.utc)
    assert port_list.modification_time == datetime(2026, 7, 9, 10, 20, 5, tzinfo=timezone.utc)
    assert port_list.writable is False
    assert port_list.in_use is True
    assert port_list.predefined is True

    # --- Permissions ---
    assert len(port_list.permissions) == 1
    assert port_list.permissions[0].name == "Everything"

    # --- Port Count ---
    assert port_list.port_count.all == 5836
    assert port_list.port_count.tcp == 5836
    assert port_list.port_count.udp == 0
