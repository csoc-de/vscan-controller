import os
from datetime import datetime, timezone

from app.models.tasks import Task


def test_task_from_real_xml_file():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "task.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    task = Task.from_xml(xml_content)

    # --- Top-Level ---
    assert task.id == "ab2a4855-92da-48f3-a6e7-eda82d7a1533"
    assert task.owner.name == "admin"
    assert task.name == "Task:HOME without Gast network:0bc7146f-ec89-4977-83e5-75d33a67ae62"
    assert task.comment == "Scan my home network without gast network"
    assert task.creation_time == datetime(2026, 7, 20, 10, 17, 54, tzinfo=timezone.utc)
    assert task.modification_time == datetime(2026, 7, 20, 10, 17, 54, tzinfo=timezone.utc)
    assert task.writable is True
    assert task.in_use is False
    assert task.alterable is True
    assert task.usage_type == "scan"
    assert task.status == "Done"
    assert task.progress == -1
    assert task.report_count.count == 1
    assert task.report_count.finished == 1
    assert task.trend is None
    assert task.schedule_periods == 0

    # --- Observers ---
    assert task.observers.user_list is None
    assert task.observers.groups is None
    assert task.observers.rules is None

    # --- Permissions ---
    assert len(task.permissions) == 1
    assert task.permissions[0].name == "Everything"

    # --- Config ---
    assert task.config.id == "daba56c8-73ec-11df-a475-002264764cea"
    assert task.config.name == "Full and fast"
    assert task.config.trash is False

    # --- Target ---
    assert task.target.id == "70465d32-2f65-4c34-944b-2e8b10432aee"
    assert task.target.name == "Target:HOME without Gast network:dc4f38be-bd66-4d68-b5f8-ff5cec315cbf"
    assert task.target.trash is False

    # --- Scanner ---
    assert task.scanner.id == "08b69003-5fc2-4037-a479-93b440211c73"
    assert task.scanner.name == "OpenVAS Default"
    assert task.scanner.type == 2
    assert task.scanner.trash is False

    # --- Schedule ---
    assert task.schedule.id == "22a9fe85-373e-4a32-a46f-589a405d7dc2"
    assert task.schedule.name == "Schedule:HOME without Gast network:5dd6a4ca-5733-4a5c-a5a7-fa09c83ab966"
    assert task.schedule.trash is False
    assert task.schedule.timezone == "Europe/Berlin"
    # icalendar ist ein großes iCalendar-Block — evtl. nur auf Existenz prüfen
    assert task.schedule.icalendar is not None
    assert ("BEGIN:VCALENDAR\\nVERSION:2.0\\nPRODID:-//Greenbone.net//NONSGML Greenbone Security"
            in task.schedule.icalendar)
    assert (
            "20260720T131800\\nDURATION:PT2H42M\\nRRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR\\nUID:b867dd24-c20b-4828-adfb-fafb7c9252fa\\nDTSTAMP:20260720T131731Z\\nEND:VEVENT\\nEND:VCALENDAR\\n"
            in task.schedule.icalendar)

    # --- Last Report ---
    assert task.last_report.id == "1cf07104-5cbd-440c-b06a-4388ecc4d31c"
    assert task.last_report.timestamp == datetime(2026, 7, 20, 11, 18, 11, tzinfo=timezone.utc)
    assert task.last_report.scan_start == datetime(2026, 7, 20, 11, 18, 32, tzinfo=timezone.utc)
    assert task.last_report.scan_end == datetime(2026, 7, 20, 11, 44, 29, tzinfo=timezone.utc)
    assert task.last_report.severity == 7.5
    assert task.last_report.result_count.critical.count == 0
    assert task.last_report.result_count.hole.count == 1
    assert task.last_report.result_count.hole.deprecated is True
    assert task.last_report.result_count.high.count == 1
    assert task.last_report.result_count.info.count == 3
    assert task.last_report.result_count.info.deprecated is True
    assert task.last_report.result_count.low.count == 3
    assert task.last_report.result_count.log.count == 37
    assert task.last_report.result_count.warning.count == 0
    assert task.last_report.result_count.warning.deprecated is True
    assert task.last_report.result_count.medium.count == 0
    assert task.last_report.result_count.false_positive.count == 0

    # --- Preferences ---
    assert len(task.preferences) == 7

    prefs = {p.scanner_name: p for p in task.preferences}
    assert prefs["max_checks"].name == "Maximum concurrently executed NVTs per host"
    assert prefs["max_checks"].value == "4"

    assert prefs["max_hosts"].name == "Maximum concurrently scanned hosts"
    assert prefs["max_hosts"].value == "20"

    assert prefs["in_assets"].name == "Add results to Asset Management"
    assert prefs["in_assets"].value == "yes"

    assert prefs["assets_apply_overrides"].name == "Apply Overrides when adding Assets"
    assert prefs["assets_apply_overrides"].value == "yes"

    assert prefs["assets_min_qod"].name == "Min QOD when adding Assets"
    assert prefs["assets_min_qod"].value == "70"

    assert prefs["auto_delete"].name == "Auto Delete Reports"
    assert prefs["auto_delete"].value == "keep"

    assert prefs["auto_delete_data"].name == "Auto Delete Reports Data"
    assert prefs["auto_delete_data"].value == "5"
