import os
from datetime import datetime, timezone
from app.models.reports import Report

def test_report_from_real_xml_file():
    xml_path = os.path.join(os.path.dirname(__file__), "files", "report.xml")

    assert os.path.exists(xml_path)

    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    report = Report.from_xml(xml_content)
    report_id = "a5f95af4-fa6d-4201-8d7d-4a9c31ba9a15"

    assert report.id == report_id
    assert report.name == "2026-07-07T13:05:49Z"
    assert report.comment == None
    assert report.writable is False
    assert report.in_use is False
    assert report.creation_time == datetime(2026, 7, 7, 13, 5, 49, tzinfo=timezone.utc)
    assert report.modification_time == datetime(2026, 7, 7, 13, 23, 36, tzinfo=timezone.utc)

    assert report.owner.name == "admin"
    assert report.task.id == "6b099e87-69d5-442e-8440-3704c7dfd856"
    assert report.task.name == "Task:Scan local Network:6b099e87-69d5-442e-8440-3704c7dfd856"

    inner = report.inner_report
    assert inner.id == report_id
    assert inner.gmp.version == "22.7"

    if inner.sort_field:
        assert inner.sort_field.text == "severity"
        assert inner.sort_field.order == "descending"

    if inner.filters:
        assert inner.filters.term == "levels=chml rows=100 min_qod=70 first=1 sort-reverse=severity result_hosts_only=0"
        assert "Critical" in inner.filters.filter

    assert inner.scan_run_status == "Done"
    assert inner.hosts.count == 1
    assert inner.vulns.count == 40

    assert inner.task.target.id == "255018b7-0929-449b-9588-2265fa04be91"
    assert inner.task.target.name == "Target:Scan local Network:255018b7-0929-449b-9588-2265fa04be91"

    assert  inner.timestamp == datetime(2026, 7, 7, 13, 5, 49, tzinfo=timezone.utc)
    assert  inner.scan_start == datetime(2026, 7, 7, 13, 6, 3, tzinfo=timezone.utc)
    assert  inner.timezone_abbrev == "UTC"

    assert inner.ports is not None
    assert inner.ports.count == 4
    assert len(inner.ports.ports) == 4

    port_0 = inner.ports.ports[0]
    # assert port_0.text == "general/icmp" # FIXME: I am the text of the element and can not be read
    assert port_0.host == "192.168.100.144"
    assert port_0.severity == 2.1
    assert port_0.threat == "Low"

    port_2 = inner.ports.ports[2]
    # assert port_2.text == "6379/tcp" # FIXME: I am the text of the element and can not be read
    assert port_2.host == "192.168.100.144"
    assert port_2.severity == 7.5
    assert port_2.threat == "High"

    assert inner.results is not None
    assert len(inner.results.results) == 4

    result_0 = inner.results.results[0]
    assert result_0.id == "5bf060d7-0a86-4cb0-89ff-211e3e245117"
    assert result_0.name == "Redis Server No Password (TCP)"
    assert result_0.threat == "High"
    assert result_0.severity == 7.5

    assert result_0.host.ip == "192.168.100.144"
    assert result_0.host.asset.asset_id == "72263a69-03bb-4fda-80b7-d427663c06cf"

    assert result_0.nvt.oid == "1.3.6.1.4.1.25623.1.0.105291"
    assert result_0.nvt.name == "Redis Server No Password (TCP)"
    assert result_0.nvt.cvss_base == 7.5
    assert result_0.nvt.cvss_base == 7.5
    assert 'cvss_base_vector=AV' in " ".join(result_0.nvt.tags.split())

    if inner.tls_certificates:
        assert inner.tls_certificates.sha256_fingerprint is None
