import os
from datetime import datetime, timezone

from app.models.reports import Report, ReportReportFilterKeyword, ReportReportResultNVTReference


def test_report_from_real_xml_file():
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
    assert port_0.port == "general/icmp"
    assert port_0.host == "192.168.100.144"
    assert port_0.severity == 2.1
    assert port_0.threat == "Low"

    port_1 = inner_report.ports.ports[1]
    assert port_1.port == "general/tcp"
    assert port_1.host == "192.168.100.144"
    assert port_1.severity == 2.6
    assert port_1.threat == "Low"

    port_2 = inner_report.ports.ports[2]
    assert port_2.port == "6379/tcp"
    assert port_2.host == "192.168.100.144"
    assert port_2.severity == 7.5
    assert port_2.threat == "High"

    port_3 = inner_report.ports.ports[3]
    assert port_3.port == "22/tcp"
    assert port_3.host == "192.168.100.144"
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
