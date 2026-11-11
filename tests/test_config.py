import os
from datetime import UTC, datetime

from app.models.configs import Config


def test_config_parsing_xml_to_model():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "config.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    config = Config.from_xml(xml_content)

    # --- Top-Level ---
    assert config.id == "daba56c8-73ec-11df-a475-002264764cea"
    assert config.owner.name == "admin"
    assert config.name == "Full and fast"
    assert (
        config.comment
        == "Most NVT\\'s; optimized by using previously collected information. Version 20201215."
    )
    assert config.creation_time == datetime(2026, 4, 24, 13, 19, 31, tzinfo=UTC)
    assert config.modification_time == datetime(2026, 7, 9, 10, 20, 15, tzinfo=UTC)
    assert config.writable is False
    assert config.in_use is True
    assert config.type == 0
    assert config.usage_type == "scan"
    assert config.predefined is False

    # --- Permissions ---
    assert len(config.permissions) == 1
    assert config.permissions[0].name == "Everything"

    # --- Counts ---
    assert config.family_count.value == 60
    assert config.family_count.growing is True

    assert config.nvt_count.value == 175648
    assert config.nvt_count.growing is True
