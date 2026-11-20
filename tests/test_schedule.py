import os
from datetime import UTC, datetime

from vscan_controller.models.schedules import Schedule


def test_schedule_parsing_xml_to_model():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "schedule.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    schedule = Schedule.from_xml(xml_content)

    # --- Top-Level ---
    assert schedule.id == "22a9fe85-373e-4a32-a46f-589a405d7dc2"
    assert schedule.owner.name == "admin"
    assert (
        schedule.name == "Schedule:HOME without Gast network:5dd6a4ca-5733-4a5c-a5a7-fa09c83ab966"
    )
    assert schedule.comment == "Scan my home network without gast network"
    assert schedule.creation_time == datetime(2026, 7, 20, 10, 14, 26, tzinfo=UTC)
    assert schedule.modification_time == datetime(2026, 7, 20, 11, 17, 31, tzinfo=UTC)
    assert schedule.writable is True
    assert schedule.in_use is False
    assert schedule.timezone == "Europe/Berlin"
    assert schedule.icalendar is not None
    assert (
        "BEGIN:VCALENDAR\\nVERSION:2.0\\nPRODID:-//Greenbone.net//NONSGML Greenbone Security Manager"
        in schedule.icalendar
    )
    assert (
        "20260720T131800\\nDURATION:PT2H42M\\nRRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR\\nUID:b867dd24-c20b-4828-adfb-fafb7c9252fa\\nDTSTAMP:20260720T131731Z\\nEND:VEVENT\\nEND:VCALENDAR\\n"
        in schedule.icalendar
    )

    # --- Permissions ---
    assert len(schedule.permissions) == 1
    assert schedule.permissions[0].name == "Everything"
