import os
from datetime import datetime, timezone

from app.models.reports import Report, ReportReportFilterKeyword, ReportReportResultNVTReference


def test_report_parsing_xml_to_model():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "report.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    report = Report.from_xml(xml_content)
    report_id = "a5f95af4-fa6d-4201-8d7d-4a9c31ba9a15"

    assert report.id == report_id
    assert report.name == "2026-07-07T13:05:49Z"
    assert report.comment is None
    assert report.writable is False
    assert report.in_use is False
    assert report.creation_time == datetime(2026, 7, 7, 13, 5, 49, tzinfo=timezone.utc)
    assert report.modification_time == datetime(2026, 7, 7, 13, 23, 36, tzinfo=timezone.utc)

    assert report.owner.name == "admin"
    assert report.task.id == "6b099e87-69d5-442e-8440-3704c7dfd856"
    assert report.task.name == "Task:Scan local Network:6b099e87-69d5-442e-8440-3704c7dfd856"

    inner_report = report.report
    assert inner_report.id == report_id
    assert inner_report.gmp.version == "22.7"

    if inner_report.sort_field:
        assert inner_report.sort_field.text == "severity"
        assert inner_report.sort_field.order == "descending"

    if inner_report.filters:
        assert inner_report.filters.term == "levels=chml rows=100 min_qod=70 first=1 sort-reverse=severity result_hosts_only=0"
        assert "Critical" in inner_report.filters.filter
        assert "High" in inner_report.filters.filter
        assert "Medium" in inner_report.filters.filter
        assert "Low" in inner_report.filters.filter

        keyword = ReportReportFilterKeyword
        keyword.column = "apply_overrides"
        keyword.relation = "="
        keyword.value = "0"
        assert keyword in inner_report.filters.keywords

        keyword = ReportReportFilterKeyword
        keyword.column = "levels"
        keyword.relation = "="
        keyword.value = "chml"
        assert keyword in inner_report.filters.keywords

        keyword = ReportReportFilterKeyword
        keyword.column = "rows"
        keyword.relation = "="
        keyword.value = "100"
        assert keyword in inner_report.filters.keywords

        keyword = ReportReportFilterKeyword
        keyword.column = "min_qod"
        keyword.relation = "="
        keyword.value = "70"
        assert keyword in inner_report.filters.keywords

        keyword = ReportReportFilterKeyword
        keyword.column = "first"
        keyword.relation = "="
        keyword.value = "1"
        assert keyword in inner_report.filters.keywords

        keyword = ReportReportFilterKeyword
        keyword.column = "sort-reverse"
        keyword.relation = "="
        keyword.value = "severity"
        assert keyword in inner_report.filters.keywords

        keyword = ReportReportFilterKeyword
        keyword.column = "result_hosts_only"
        keyword.relation = "="
        keyword.value = "0"
        assert keyword in inner_report.filters.keywords

    assert inner_report.scan_run_status == "Done"
    assert inner_report.hosts.count == 1
    assert inner_report.closed_cves.count == 0
    assert inner_report.vulns.count == 40
    assert inner_report.os.count == 1
    assert inner_report.apps.count == 3
    assert inner_report.ssl_certs.count == 0

    assert inner_report.task.id == "6b099e87-69d5-442e-8440-3704c7dfd856"
    assert inner_report.task.name == "Task:Scan local Network:6b099e87-69d5-442e-8440-3704c7dfd856"
    assert inner_report.task.comment is None
    assert inner_report.task.progress == 100
    assert inner_report.task.target.id == "255018b7-0929-449b-9588-2265fa04be91"
    assert inner_report.task.target.trash is False
    assert inner_report.task.target.name == "Target:Scan local Network:255018b7-0929-449b-9588-2265fa04be91"
    assert inner_report.task.target.comment is None

    assert inner_report.timestamp == datetime(2026, 7, 7, 13, 5, 49, tzinfo=timezone.utc)
    assert inner_report.scan_start == datetime(2026, 7, 7, 13, 6, 3, tzinfo=timezone.utc)
    assert inner_report.timezone == "Coordinated Universal Time"
    assert inner_report.timezone_abbrev == "UTC"

    assert inner_report.ports is not None
    assert inner_report.ports.count == 4
    assert len(inner_report.ports.ports) == 4

    port_0 = inner_report.ports.ports[0]
    assert port_0.host_port == "general/icmp"
    assert port_0.host_name == "192.168.100.144"
    assert port_0.severity == 2.1
    assert port_0.threat == "Low"

    port_1 = inner_report.ports.ports[1]
    assert port_1.host_port == "general/tcp"
    assert port_1.host_name == "192.168.100.144"
    assert port_1.severity == 2.6
    assert port_1.threat == "Low"

    port_2 = inner_report.ports.ports[2]
    assert port_2.host_port == "6379/tcp"
    assert port_2.host_name == "192.168.100.144"
    assert port_2.severity == 7.5
    assert port_2.threat == "High"

    port_3 = inner_report.ports.ports[3]
    assert port_3.host_port == "22/tcp"
    assert port_3.host_name == "192.168.100.144"
    assert port_3.severity == 2.6
    assert port_3.threat == "Low"

    assert inner_report.results is not None
    assert len(inner_report.results.results) == 4

    result_0 = inner_report.results.results[0]
    assert result_0.id == "5bf060d7-0a86-4cb0-89ff-211e3e245117"
    assert result_0.name == "Redis Server No Password (TCP)"
    assert result_0.owner.name == "admin"
    assert result_0.modification_time == datetime(2026, 7, 7, 13, 8, 21, tzinfo=timezone.utc)
    assert result_0.comment is None
    assert result_0.creation_time == datetime(2026, 7, 7, 13, 8, 21, tzinfo=timezone.utc)
    assert result_0.port == "6379/tcp"
    assert result_0.scan_nvt_version == datetime(2025, 11, 25, 5, 40, 35, tzinfo=timezone.utc)
    assert result_0.threat == "High"
    assert result_0.severity == 7.5
    assert result_0.description == "Redis Server is not protected with a password.\\n"
    assert result_0.original_threat == "High"
    assert result_0.original_severity == 7.5
    assert result_0.compliance == "undefined"

    assert result_0.host.host == "192.168.100.144"
    assert result_0.host.hostname is None
    assert result_0.host.asset.asset_id == "72263a69-03bb-4fda-80b7-d427663c06cf"

    assert result_0.nvt.oid == "1.3.6.1.4.1.25623.1.0.105291"
    assert result_0.nvt.type == "nvt"
    assert result_0.nvt.name == "Redis Server No Password (TCP)"
    assert result_0.nvt.family == "Databases"
    assert result_0.nvt.cvss_base == 7.5
    assert "cvss_base_vector=AV:N/AC:L/Au:N/C:P/I:P/A:P|summary=The remote Redis" in result_0.nvt.tags
    assert "1.3.6.1.4.1.25623.1.0.12288)|solution_type=Workaround" in result_0.nvt.tags
    assert result_0.nvt.refs is None

    assert result_0.nvt.severities.score == 7.5
    assert result_0.nvt.severities.severities[0].type == "cvss_base_v2"
    assert result_0.nvt.severities.severities[0].date == datetime(2015, 6, 5, 13, 48, 46, tzinfo=timezone.utc)
    assert result_0.nvt.severities.severities[0].score == 7.5
    assert result_0.nvt.severities.severities[0].origin is None
    assert result_0.nvt.severities.severities[0].value == "AV:N/AC:L/Au:N/C:P/I:P/A:P"
    assert result_0.nvt.solution.type == "Workaround"
    assert result_0.nvt.solution.solution == "Set password."

    assert result_0.qod.value == 99
    assert result_0.qod.type is None

    result_1 = inner_report.results.results[1]
    ref = ReportReportResultNVTReference
    ref.type = "url"
    ref.id = "https://datatracker.ietf.org/doc/html/rfc1323"
    assert ref in result_1.nvt.refs
    ref = ReportReportResultNVTReference
    ref.type = "url"
    ref.id = "https://datatracker.ietf.org/doc/html/rfc7323"
    assert ref in result_1.nvt.refs
    ref = ReportReportResultNVTReference
    ref.type = "url"
    ref.id = "https://web.archive.org/web/20151213072445/http://www.microsoft.com/en-us/download/details.aspx?id=9152"
    assert ref in result_1.nvt.refs
    ref = ReportReportResultNVTReference
    ref.type = "url"
    ref.id = "https://www.fortiguard.com/psirt/FG-IR-16-090"
    assert ref in result_1.nvt.refs

    result_2 = inner_report.results.results[2]
    assert result_2.detection.result.id == "a8c3df12-9775-4419-a324-1f8c0c29b614"
    assert result_2.detection.result.details[0].name == "product"
    assert result_2.detection.result.details[0].value == "cpe:/a:ietf:secure_shell_protocol"
    assert result_2.detection.result.details[1].name == "location"
    assert result_2.detection.result.details[1].value == "22/tcp"
    assert result_2.detection.result.details[2].name == "source_oid"
    assert result_2.detection.result.details[2].value == "1.3.6.1.4.1.25623.1.0.105565"
    assert result_2.detection.result.details[3].name == "source_name"
    assert result_2.detection.result.details[3].value == "SSH Protocol Algorithms Supported"

    if inner_report.tls_certificates:
        assert inner_report.tls_certificates.sha256_fingerprint is None


def test_report_parsing_xml_to_model_without_reports():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "report_2.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    report = Report.from_xml(xml_content)
    assert report.content_type == "text/xml"
    assert report.extension == "xml"
    assert report.id == "8b7e9334-b914-4a77-879b-74f18841f131"
    assert report.format_id == "a994b278-1f62-11e1-96ac-406186ea4fc5"
    assert report.config_id == ""
    assert report.owner.name == "admin"
    assert report.name == "2026-07-30T14:54:16Z"
    assert report.comment is None
    assert report.creation_time == datetime(2026, 7, 30, 14, 54, 16, tzinfo=timezone.utc)
    assert report.modification_time == datetime(2026, 7, 30, 14, 55, 11, tzinfo=timezone.utc)

    # --- Task ---
    assert report.task.id == "2783024a-925f-4ff9-8399-01051e794905"
    assert report.task.name == "Task:Test 3 :a822155c-d36a-4944-9941-a9cb05890210"

    # --- Report Format ---
    assert report.report_format.id == "a994b278-1f62-11e1-96ac-406186ea4fc5"
    assert report.report_format.name == "XML"

    inner_report = report.report
    assert inner_report.id == "8b7e9334-b914-4a77-879b-74f18841f131"
    assert inner_report.gmp.version == "22.7"
    assert inner_report.sort_field.text == "severity"
    assert inner_report.sort_field.order == "descending"

    assert inner_report.filters.id == "0"
    assert (inner_report.filters.term ==
            "apply_overrides=0 levels=chml rows=1000 min_qod=70 first=1 sort-reverse=severity result_hosts_only=0 notes=1 overrides=1")
    assert inner_report.filters.filter[0] == "Critical"
    assert inner_report.filters.filter[1] == "High"
    assert inner_report.filters.filter[2] == "Medium"
    assert inner_report.filters.filter[3] == "Low"

    keyword = ReportReportFilterKeyword
    keyword.column = "apply_overrides"
    keyword.relation = "="
    keyword.value = "0"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "levels"
    keyword.relation = "="
    keyword.value = "chml"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "rows"
    keyword.relation = "="
    keyword.value = "1000"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "min_qod"
    keyword.relation = "="
    keyword.value = "70"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "first"
    keyword.relation = "="
    keyword.value = "1"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "sort-reverse"
    keyword.relation = "="
    keyword.value = "severity"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "result_hosts_only"
    keyword.relation = "="
    keyword.value = "0"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "notes"
    keyword.relation = "="
    keyword.value = "1"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "overrides"
    keyword.relation = "="
    keyword.value = "1"
    assert keyword in inner_report.filters.keywords

    assert inner_report.scan_run_status == "Stopped"
    assert inner_report.hosts.count == 0
    assert inner_report.closed_cves.count == 0
    assert inner_report.vulns.count == 0
    assert inner_report.os.count == 0
    assert inner_report.apps.count == 0
    assert inner_report.ssl_certs.count == 0

    assert inner_report.task.id == "2783024a-925f-4ff9-8399-01051e794905"
    assert inner_report.task.name == "Task:Test 3 :a822155c-d36a-4944-9941-a9cb05890210"
    assert inner_report.task.comment == "Test TEst Test"
    assert inner_report.task.target.id == "c8b15140-2460-4885-9268-8b3d3da0c639"
    assert inner_report.task.target.trash is False
    assert inner_report.task.target.name == "Target:Test 3 :f7cc42fd-aec7-40b4-9b31-c7c0bd69c4c7"
    assert inner_report.task.target.comment == "Test TEst Test"
    assert inner_report.task.progress == 0

    assert inner_report.timestamp == datetime(2026, 7, 30, 14, 54, 16, tzinfo=timezone.utc)
    assert inner_report.scan_start == datetime(2026, 7, 30, 14, 54, 33, tzinfo=timezone.utc)
    assert inner_report.timezone == "Coordinated Universal Time"
    assert inner_report.timezone_abbrev == "UTC"

    assert inner_report.ports.max == 1000
    assert inner_report.ports.start == 1
    assert inner_report.ports.count == 0

    assert inner_report.results is not None

    assert inner_report.results.max == 1000
    assert inner_report.results.start == 1

    # --- Result Count ---
    assert inner_report.result_count.count == 0
    assert inner_report.result_count.full == 0
    assert inner_report.result_count.filtered == 0
    assert inner_report.result_count.critical.full == 0
    assert inner_report.result_count.critical.filtered == 0
    assert inner_report.result_count.hole.full == 0
    assert inner_report.result_count.hole.filtered == 0
    assert inner_report.result_count.high.full == 0
    assert inner_report.result_count.high.filtered == 0
    assert inner_report.result_count.info.full == 0
    assert inner_report.result_count.info.filtered == 0
    assert inner_report.result_count.low.full == 0
    assert inner_report.result_count.low.filtered == 0
    assert inner_report.result_count.log.full == 0
    assert inner_report.result_count.log.filtered == 0
    assert inner_report.result_count.warning.full == 0
    assert inner_report.result_count.warning.filtered == 0
    assert inner_report.result_count.medium.full == 0
    assert inner_report.result_count.medium.filtered == 0
    assert inner_report.result_count.false_positive.full == 0
    assert inner_report.result_count.false_positive.filtered == 0

    # --- Severity ---
    assert inner_report.severity.full == -99.0
    assert inner_report.severity.filtered == -99.0

    # --- TLS Certificates ---
    assert inner_report.tls_certificates.sha256_fingerprint is None

    # --- Scan End ---
    assert inner_report.scan_end == datetime(2026, 7, 30, 14, 55, 12, tzinfo=timezone.utc)

    # --- Errors ---
    assert inner_report.errors.count == 0

    # --- Empty Report Format at End ---
    assert inner_report.report_format is None


def test_report_parsing_xml_to_model_2():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "report_3.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    report = Report.from_xml(xml_content)
    assert report.content_type == "application/xml"
    assert report.extension == ""
    assert report.id == "1ecb8a04-f662-4e2a-85c9-88a89a5eced4"
    assert report.format_id == ""
    assert report.config_id == ""
    assert report.owner.name == "admin"
    assert report.name == "2026-08-05T13:18:38Z"
    assert report.comment is None
    assert report.creation_time == datetime(2026, 8, 5, 13, 18, 38, tzinfo=timezone.utc)
    assert report.modification_time == datetime(2026, 8, 5, 13, 27, 51, tzinfo=timezone.utc)

    # --- Task (outer) ---
    assert report.task.id == "35a782b4-902d-4876-944c-fe9b74a33351"
    assert report.task.name == "Task:Test 26:6a4ec856-59cb-468d-bc2b-28cff9e3f4f1"

    inner_report = report.report
    assert inner_report.id == "1ecb8a04-f662-4e2a-85c9-88a89a5eced4"
    assert inner_report.gmp.version == "22.7"
    assert inner_report.sort_field.text == "name\n                "
    assert inner_report.sort_field.order == "ascending"

    # --- Filters ---
    assert inner_report.filters.id == ""
    assert (inner_report.filters.term ==
            "apply_overrides=0 levels=hmlg min_qod=0 first=1 rows=10 sort=name")
    assert inner_report.filters.filter[0] == "High"
    assert inner_report.filters.filter[1] == "Medium"
    assert inner_report.filters.filter[2] == "Low"
    assert inner_report.filters.filter[3] == "Log"

    keyword = ReportReportFilterKeyword
    keyword.column = "apply_overrides"
    keyword.relation = "="
    keyword.value = "0"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "levels"
    keyword.relation = "="
    keyword.value = "hmlg"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "min_qod"
    keyword.relation = "="
    keyword.value = "0"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "first"
    keyword.relation = "="
    keyword.value = "1"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "rows"
    keyword.relation = "="
    keyword.value = "10"
    assert keyword in inner_report.filters.keywords

    keyword = ReportReportFilterKeyword
    keyword.column = "sort"
    keyword.relation = "="
    keyword.value = "name"
    assert keyword in inner_report.filters.keywords

    assert inner_report.scan_run_status == "Stopped"
    assert inner_report.hosts.count == 1
    assert inner_report.closed_cves.count == 0
    assert inner_report.vulns.count == 30
    assert inner_report.os.count == 0
    assert inner_report.apps.count == 0
    assert inner_report.ssl_certs.count == 5

    # --- Task (inner) ---
    assert inner_report.task.id == "35a782b4-902d-4876-944c-fe9b74a33351"
    assert inner_report.task.name == "Task:Test 26:6a4ec856-59cb-468d-bc2b-28cff9e3f4f1"
    assert inner_report.task.comment is None
    assert inner_report.task.target.id == "266cd0f7-9471-41bb-a5a4-44e5d67fb19a"
    assert inner_report.task.target.trash is False
    assert inner_report.task.target.name == "Target:Test 26:7cae6d7b-b97a-4947-b51a-acdc400c9e4d"
    assert inner_report.task.target.comment is None
    assert inner_report.task.progress == 22

    assert inner_report.timestamp == datetime(2026, 8, 5, 13, 18, 38, tzinfo=timezone.utc)
    assert inner_report.scan_start == datetime(2026, 8, 5, 13, 18, 52, tzinfo=timezone.utc)
    assert inner_report.timezone == "Coordinated Universal Time"
    assert inner_report.timezone_abbrev == "UTC"

    # --- Ports ---
    assert inner_report.ports.max == 10
    assert inner_report.ports.start == 1
    assert inner_report.ports.count == 15
    assert inner_report.ports.ports is not None
    assert len(inner_report.ports.ports) == 16

    # Port 443/tcp (Index 0)
    port_443 = inner_report.ports.ports[0]
    assert port_443.host_name == "192.168.1.119"
    assert port_443.host_port == "443/tcp"
    assert port_443.severity == 0.0
    assert port_443.threat == "Log"

    # Port 7022/tcp (Index 4)
    port_7022 = inner_report.ports.ports[4]
    assert port_7022.host_name == "192.168.1.119"
    assert port_7022.host_port == "7022/tcp"
    assert port_7022.severity == 5.9
    assert port_7022.threat == "Medium"

    # Port 6379/tcp (Index 9)
    port_6379 = inner_report.ports.ports[9]
    assert port_6379.host_name == "192.168.1.119"
    assert port_6379.host_port == "6379/tcp"
    assert port_6379.severity == 8.8
    assert port_6379.threat == "High"

    # Port 1515/tcp (Index 10)
    port_1515 = inner_report.ports.ports[10]
    assert port_1515.host_name == "192.168.1.119"
    assert port_1515.host_port == "1515/tcp"
    assert port_1515.severity == 7.5
    assert port_1515.threat == "High"

    # Port 22/tcp (Index 8)
    port_22 = inner_report.ports.ports[8]
    assert port_22.host_name == "192.168.1.119"
    assert port_22.host_port == "22/tcp"
    assert port_22.severity == 5.9
    assert port_22.threat == "Medium"

    # --- Results ---
    assert inner_report.results is not None
    assert inner_report.results.max == -1
    assert inner_report.results.start == 1
    assert len(inner_report.results.results) == 59

    # Index 0: AMQP Detection
    result = inner_report.results.results[0]
    assert result.id == "ce344907-3d56-4916-8042-39bf6e31641f"
    assert result.name == "Advanced Message Queuing Protocol (AMQP) Detection (TCP)"
    assert result.owner.name == "admin"
    assert result.host.host == "192.168.1.119\n                    "
    assert result.port == "5673/tcp"
    assert result.nvt.oid == "1.3.6.1.4.1.25623.1.0.105030"
    assert result.nvt.name == "Advanced Message Queuing Protocol (AMQP) Detection (TCP)"
    assert result.nvt.family == "Service detection"
    assert result.nvt.cvss_base == 0.0
    assert result.threat == "Log"
    assert result.severity == 0.0
    assert result.qod.value == 80
    assert result.scan_nvt_version == datetime(2025, 3, 27, 5, 38, 50, tzinfo=timezone.utc)
    assert result.original_threat == "Log"
    assert result.original_severity == 0
    assert result.compliance == "undefined"

    # Index 1: OpenSSH DoS Vulnerability (7022/tcp)
    result = inner_report.results.results[1]
    assert result.id == "7d79b6de-d488-4286-94a6-b8c2de1779e9"
    assert result.name == "OpenBSD OpenSSH 9.5p1 - 9.9p1 DoS Vulnerability"
    assert result.host.host == "192.168.1.119\n                    "
    assert result.port == "7022/tcp"
    assert result.nvt.oid == "1.3.6.1.4.1.25623.1.0.114947"
    assert result.nvt.family == "Denial of Service"
    assert result.nvt.cvss_base == 5.9
    assert result.threat == "Medium"
    assert result.severity == 5.9
    assert result.qod.value == 30
    assert result.nvt.solution.type == "VendorFix"
    assert result.nvt.solution.solution == "Update to version 9.9p2 or later."
    assert result.original_threat == "Medium"
    assert result.original_severity == 5.9

    # Index 2: OpenSSH DoS Vulnerability (22/tcp)
    result = inner_report.results.results[2]
    assert result.id == "753229a4-adef-49c1-9b3d-b4678fe8daf3"
    assert result.name == "OpenBSD OpenSSH 9.5p1 - 9.9p1 DoS Vulnerability"
    assert result.port == "22/tcp"
    assert result.nvt.oid == "1.3.6.1.4.1.25623.1.0.114947"
    assert result.threat == "Medium"
    assert result.severity == 5.9
    assert result.qod.value == 30


def test_report_parsing_xml_to_model_ports_xml_severity_tail():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "report_4.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    report = Report.from_xml(xml_content)
    assert report.content_type == "application/xml"
    assert report.extension == ""
    assert report.id == "1ecb8a04-f662-4e2a-85c9-88a89a5eced4"
    assert report.format_id == ""
    assert report.config_id == ""
    assert report.owner.name == "admin"
    assert report.name == "2026-08-05T13:18:38Z"
    assert report.comment is None
    assert report.creation_time == datetime(2026, 8, 5, 13, 18, 38, tzinfo=timezone.utc)
    assert report.modification_time == datetime(2026, 8, 5, 13, 27, 51, tzinfo=timezone.utc)

    inner_report = report.report

    # Port 443/tcp (Index 0)
    port_443 = inner_report.ports.ports[0]
    assert port_443.host_name == "192.168.1.119"
    assert port_443.host_port == "443/tcp"
    assert port_443.severity == 0.0
    assert port_443.threat == "Log"


def test_report_parsing_xml_to_model_ports_xml_threat_tail():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "report_5.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    report = Report.from_xml(xml_content)
    assert report.content_type == "application/xml"
    assert report.extension == ""
    assert report.id == "1ecb8a04-f662-4e2a-85c9-88a89a5eced4"
    assert report.format_id == ""
    assert report.config_id == ""
    assert report.owner.name == "admin"
    assert report.name == "2026-08-05T13:18:38Z"
    assert report.comment is None
    assert report.creation_time == datetime(2026, 8, 5, 13, 18, 38, tzinfo=timezone.utc)
    assert report.modification_time == datetime(2026, 8, 5, 13, 27, 51, tzinfo=timezone.utc)

    inner_report = report.report

    # Port 443/tcp (Index 0)
    port_443 = inner_report.ports.ports[0]
    assert port_443.host_name == "192.168.1.119"
    assert port_443.host_port == "443/tcp"
    assert port_443.severity == 0.0
    assert port_443.threat == "Log"
