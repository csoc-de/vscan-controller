from __future__ import annotations

from datetime import datetime
from typing import Annotated

from lxml.etree import _Element as Element
from pydantic import BaseModel, Field, computed_field, constr
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from app.models.base import Owner, Permission, UserTags


class Task(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: str = element()


class ReportFormat(BaseXmlModel, search_mode="unordered", tag="report_format"):
    id: str = attr()
    name: str = element()


class ReportReportGMP(BaseXmlModel, search_mode="unordered", tag="gmp"):
    version: str = element()


class ReportReportFormatParam(BaseXmlModel, search_mode="unordered", tag="param"):
    name: str = element()
    value: str = element()


class ReportReportField(BaseXmlModel, search_mode="unordered", tag="field"):
    text: str
    order: str = element()


class ReportReportFilterKeyword(BaseXmlModel, search_mode="unordered", tag="keyword"):
    column: str = element()
    relation: str = element()
    value: str = element()

    def __eq__(self, other):
        return (
            (self.column == other.column)
            and (self.relation == other.relation)
            and (self.value == other.value)
        )


class ReportReportFiltersDelta(BaseXmlModel, search_mode="unordered", tag="delta"):
    changed: str = element()
    gone: str = element()
    new: str = element()
    same: str = element()


class ReportReportFilters(BaseXmlModel, search_mode="unordered", tag="filters"):
    id: str | None = attr(default=None)
    term: str = element()
    phrase: str | None = element(default=None)
    notes: int | None = element(default=None)
    overrides: int | None = element(default=None)
    result_hosts_only: int | None = element(default=None)
    min_qod: str | None = element(default=None)
    delta: ReportReportFiltersDelta | None = element(default=None)
    filter: list[str] = element()
    keywords: list[ReportReportFilterKeyword] = wrapped("keywords", element(tag="keyword"))


class ReportReportDeltaReport(BaseXmlModel, search_mode="unordered", tag="report"):
    id: str = attr()
    scan_run_status: str = element()
    timestamp: datetime = element()
    scan_start: datetime = element()
    scan_end: datetime = element()


class ReportReportDelta(BaseXmlModel, search_mode="unordered", tag="delta"):
    report: ReportReportDeltaReport = element()


class ReportReportFullFiltered(BaseXmlModel, search_mode="unordered"):
    full: float = element()
    filtered: float = element()


class ReportReportResultCountFullFiltered(BaseXmlModel, search_mode="unordered"):
    deprecated: str | None = None
    full: int = element()
    filtered: int = element()


class ReportReportResultCount(BaseXmlModel, search_mode="unordered", tag="result_count"):
    count: int
    full: int = element()
    filtered: int = element()
    log: ReportReportResultCountFullFiltered = element(tag="log")
    info: ReportReportResultCountFullFiltered = element(tag="info")
    low: ReportReportResultCountFullFiltered = element(tag="low")
    medium: ReportReportResultCountFullFiltered = element(tag="medium")
    warning: ReportReportResultCountFullFiltered = element(tag="warning")
    high: ReportReportResultCountFullFiltered = element(tag="high")
    critical: ReportReportResultCountFullFiltered = element(tag="critical")
    hole: ReportReportResultCountFullFiltered = element(tag="hole")
    false_positive: ReportReportResultCountFullFiltered = element(tag="false_positive")


class ReportReportTaskTarget(BaseXmlModel, search_mode="unordered", tag="target"):
    id: str = attr()
    trash: bool = element()
    name: str = element()
    comment: str | None = element(default=None)


class ReportReportTask(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: str = element()
    comment: str | None = element(default=None)
    target: ReportReportTaskTarget = element(tag="target")
    progress: int = element()
    user_tags: UserTags | None = element(default=None, tag="user_tags")


class ReportReportPortsPort(
    BaseXmlModel, search_mode="unordered", tag="port", arbitrary_types_allowed=True
):
    port: str | None = None
    host: Annotated[Element, Field(exclude=True)] = element(
        field=Field(exclude=True, default=None)
    )  # field is excluded (fastapi)
    severity_elem: Annotated[Element, Field(exclude=True)] = element(
        field=Field(exclude=True, default=None), tag="severity", default=None
    )
    threat_elem: Annotated[Element, Field(exclude=True)] = element(
        field=Field(exclude=True, default=None), tag="threat", default=None
    )

    @computed_field(return_type=str | None)
    @property
    def host_name(self):
        return self.host.text

    @host_name.setter
    def host_name(self, name: str):
        self.host.text = name

    @computed_field(return_type=str | None)
    @property
    def host_port(self):
        if self.port is not None and self.port.strip() != "":
            return self.port
        if self.host is not None and self.host.tail.strip() != "":
            return self.host.tail.strip()
        if self.severity_elem is not None and self.severity_elem.tail.strip() != "":
            stripped = self.severity_elem.tail.strip()
            if stripped:
                return stripped
        if self.threat_elem is not None and self.threat_elem.tail.strip() != "":
            stripped = self.threat_elem.tail.strip()
            if stripped:
                return stripped
        return None

    @host_port.setter
    def host_port(self, port: str):
        self.host.tail = port

    @computed_field(return_type=float | None)
    @property
    def severity(self) -> float | None:
        if self.severity_elem is not None and self.severity_elem.text:
            try:
                return float(self.severity_elem.text.strip())
            except ValueError:
                return None
        return None

    @computed_field(return_type=str | None)
    @property
    def threat(self) -> str | None:
        if self.threat_elem is not None:
            return self.threat_elem.text
        return None


class ReportReportPorts(BaseXmlModel, search_mode="unordered", tag="ports"):
    start: int | None = attr(default=None)
    max: int | None = attr(default=None)
    count: int | None = element(default=None)
    ports: list[ReportReportPortsPort] | None = element(tag="port", default=None)


class ReportReportResultReport(BaseXmlModel, search_mode="unordered", tag="report"):
    id: str = attr()


class ReportReportAsset(BaseXmlModel, search_mode="unordered", tag="asset"):
    asset_id: str = attr()


class ReportReportResultHost(BaseXmlModel, search_mode="unordered", tag="host"):
    host: constr(strip_whitespace=True) | None = None  # type: ignore[valid-type]
    asset: ReportReportAsset = element(tag="asset")
    hostname: str | None = element(default=None)


class ReportReportResultNVTSeverity(BaseXmlModel, search_mode="unordered", tag="severity"):
    type: str = attr()
    origin: str | None = element(default=None)
    date: datetime = element()
    score: float = element()
    value: str = element()


class ReportReportResultNVTSeverities(BaseXmlModel, search_mode="unordered", tag="severities"):
    score: float = attr()
    severities: list[ReportReportResultNVTSeverity] = element(tag="severity")


class ReportReportResultNVTReference(BaseXmlModel, search_mode="unordered", tag="ref"):
    id: str = attr()
    type: str = attr()

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id


class ReportReportResultNVTSolution(BaseXmlModel, search_mode="unordered", tag="solution"):
    solution: str | None = None
    type: str | None = attr(default=None)


class ReportReportResultNVT(BaseXmlModel, search_mode="unordered", tag="nvt"):
    oid: str = attr()
    type: str = element()
    name: str = element()
    family: str = element()
    cvss_base: float = element()
    severities: ReportReportResultNVTSeverities = element()
    cpe: str | None = element(default=None)
    tags: str = element()
    refs: list[ReportReportResultNVTReference] | None = wrapped("refs", default=None, tag="ref")
    solution: ReportReportResultNVTSolution | None = element(tag="solution")


class ReportReportResultQOD(BaseXmlModel, search_mode="unordered", tag="qod"):
    value: int = element()
    type: str | None = element(default=None)


class ReportReportResultDeltaNoteNVT(BaseXmlModel, search_mode="unordered", tag="nvt"):
    oid: str = attr()
    name: str = element()
    type: str = element()


class ReportReportResultDeltaNoteText(BaseXmlModel, search_mode="unordered", tag="text"):
    excerpt: bool = attr()


class ReportReportResultDeltaNoteTask(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()


class ReportReportResultDeltaNoteResultNVT(BaseXmlModel, search_mode="unordered", tag="nvt"):
    oid: str = attr()
    name: str = element()
    type: str = element()
    cvss_base: str = element()
    severities: ReportReportResultNVTSeverities = element()
    cve: str | None = element(default=None)


class ReportReportResultDeltaNoteOrOverwriteResult(
    BaseXmlModel, search_mode="unordered", tag="result"
):
    id: str = attr()
    host: ReportReportResultHost = element()
    port: str = element()
    nvt: ReportReportResultDeltaNoteResultNVT = element()
    severity: str = element()
    threat: str = element()
    qod: ReportReportResultQOD = element()
    description: str = element()


class ReportReportResultNote(BaseXmlModel, search_mode="unordered", tag="note"):
    id: str = attr()
    permissions: list[Permission] = wrapped("permissions", element(tag="permission"))
    owner: Owner = element(tag="owner")
    nvt: ReportReportResultDeltaNoteNVT = element()
    text: ReportReportResultDeltaNoteText = element()
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    active: bool = element()
    orphan: bool = element()
    user_tags: UserTags | None = element(tag="user_tags", default=None)
    hosts: str | None = element(default=None)
    port: str | None = element(default=None)
    severity: float | None = element(default=None)
    task: ReportReportResultDeltaNoteTask | None = element(default=None)
    end_time: datetime | None = element(default=None)
    result: ReportReportResultDeltaNoteOrOverwriteResult | None = element(default=None)


class ReportReportResultOverwrite(BaseXmlModel, search_mode="unordered", tag="overwrite"):
    id: str = attr()
    permissions: list[Permission] = wrapped("permissions", element(tag="permission"))
    owner: Owner = element(tag="owner")
    nvt: ReportReportResultDeltaNoteNVT = element()
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    user_tags: UserTags | None = element(tag="user_tags", default=None)
    active: bool = element()
    orphan: bool = element()
    text: ReportReportResultDeltaNoteText = element()
    severity: str = element()
    threat: str = element()
    new_severity: str = element()
    new_threat: str = element()
    hosts: str | None = element(default=None)
    port: str | None = element(default=None)
    task: ReportReportResultDeltaNoteTask | None = element(default=None)
    end_time: datetime | None = element(default=None)
    result: ReportReportResultDeltaNoteOrOverwriteResult | None = element(default=None)


class ReportReportResultDelta(BaseXmlModel, search_mode="unordered", tag="delta"):
    result: ReportReportResult | None = element()
    diff: str = element()
    notes: list[ReportReportResultNote] | None = element(tag="note", default=None)
    overwrites: list[ReportReportResultOverwrite] | None = element(tag="overwrite", default=None)


class ReportReportResultDetectionResultDetail(BaseXmlModel, search_mode="unordered", tag="detail"):
    name: str = element()
    value: str = element()


class ReportReportResultDetectionResult(BaseXmlModel, search_mode="unordered", tag="result"):
    id: str = attr()
    details: list[ReportReportResultDetectionResultDetail] | None = wrapped(
        path="details", tag="detail", default=None
    )


class ReportReportResultDetection(BaseXmlModel, search_mode="unordered", tag="detection"):
    result: ReportReportResultDetectionResult = element()


class ReportReportResultTicket(BaseXmlModel, search_mode="unordered", tag="ticket"):
    id: str = attr()


class ReportReportResult(BaseXmlModel, search_mode="unordered", tag="result"):
    id: str = attr()
    name: str = element()
    owner: Owner = element(tag="owner")
    modification_time: datetime = element()
    comment: str | None = element(default=None)
    creation_time: datetime = element()
    detection: ReportReportResultDetection | None = element(default=None)
    host: ReportReportResultHost = element()
    port: str = element()
    nvt: ReportReportResultNVT = element()
    report: ReportReportResultReport | None = element(tag="report", default=None)
    task: ReportReportTask | None = element(tag="task", default=None)
    path: str | None = element(default=None)
    scan_nvt_version: datetime = element()
    threat: str = element()
    severity: float = element()
    qod: ReportReportResultQOD = element()
    description: str | None = element(default=None)
    original_threat: str | None = element(default=None)
    original_severity: float | None = element(default=None)
    compliance: str | None = element(default=None)
    # delta: ReportReportResultDelta | None = element(default=None)
    notes: list[ReportReportResultNote] | None = element(tag="note", default=None)
    overwrites: list[ReportReportResultOverwrite] | None = element(tag="overwrite", default=None)
    tickets: ReportReportResultTicket | None = element(tag="tickets", default=None)
    user_tags: UserTags | None = element(tag="user_tags", default=None)


class ReportReportResults(BaseXmlModel, search_mode="unordered", tag="results"):
    start: int = attr()
    max: int = attr()
    results: list[ReportReportResult] | None = element(tag="result", default=None)


class ReportReportHosts(BaseXmlModel, search_mode="unordered", tag="hosts"):
    start: int | None = attr(default=None)
    max: int | None = attr(default=None)
    count: int | None = attr(default=None)


class ReportReportCount(BaseXmlModel, search_mode="unordered"):
    count: int = element()


class ReportReportHostResultSeverity(BaseXmlModel, search_mode="unordered", tag="page"):
    text: str
    page: int = element()


class ReportReportHostResultCount(BaseXmlModel, search_mode="unordered", tag="result_count"):
    page: int = element()
    hole: ReportReportHostResultSeverity = element(tag="hole")
    warning: ReportReportHostResultSeverity = element(tag="warning")
    info: ReportReportHostResultSeverity = element(tag="info")
    log: ReportReportHostResultSeverity = element(tag="log")
    false_positive: ReportReportHostResultSeverity = element(tag="false_positive")


class ReportReportHostDetailSource(BaseXmlModel, search_mode="unordered", tag="source"):
    type: str = element()
    name: str = element()
    description: str = element()


class ReportReportHostDetail(BaseXmlModel, search_mode="unordered", tag="detail"):
    name: str = element()
    value: str = element()
    source: ReportReportHostDetailSource = element(tag="source")
    extra: str = element()


class ReportReportHost(BaseXmlModel, search_mode="unordered", tag="host"):
    ip: str = element()
    asset: ReportReportAsset = element()
    start: datetime = element()
    end: datetime = element()
    port_count: ReportReportHostResultSeverity = element(tag="port_count")
    result_count: ReportReportHostResultCount = element(tag="result_count")
    details: list[ReportReportHostDetail] = element(tag="detail")


class ReportReportTLSCertificateCertificate(
    BaseXmlModel, search_mode="unordered", tag="certificate"
):
    format: str = attr()


class ReportReportTLSCertificateHost(BaseXmlModel, search_mode="unordered", tag="host"):
    ip: str = element()
    hostname: str = element()


class ReportReportTLSCertificate(BaseXmlModel, search_mode="unordered", tag="tls_certificate"):
    name: str | None = element(default=None)
    certificate: ReportReportTLSCertificateCertificate | None = element(
        tag="certificate", default=None
    )
    sha256_fingerprint: str | None = element(default=None)
    md5_fingerprint: str | None = element(default=None)
    valid: bool | None = element(default=None)
    activation_time: datetime | None = element(default=None)
    expiration_time: datetime | None = element(default=None)
    subject_dn: str | None = element(default=None)
    issuer_dn: str | None = element(default=None)
    serial: str | None = element(default=None)
    host: ReportReportTLSCertificateHost | None = element(default=None)
    ports: list[str] | None = wrapped("ports", element(tag="port"), default=None)


class ReportReportErrorNVT(BaseXmlModel, search_mode="unordered", tag="nvt"):
    oid: str = attr()
    name: str | None = element(default=None)
    type: str | None = element(default=None)
    cvss_base: str | None = element(default=None)


class ReportReportError(BaseXmlModel, search_mode="unordered", tag="error"):
    host: ReportReportResultHost | None = element(tag="host", default=None)
    port: str | None = element(default=None)
    description: str | None = element(default=None)
    nvt: ReportReportErrorNVT | None = element(default=None)
    scan_nvt_version: str | None = element(default=None)
    severity: float | None = element(default=None)


class ReportReportErrors(BaseXmlModel, search_mode="unordered", tag="errors"):
    count: int = element()
    errors: list[ReportReportError] | None = element(tag="error", default=None)


class ReportReport(BaseXmlModel, search_mode="unordered", tag="report"):
    id: str = attr()
    type: str | None = attr(default=None)
    gmp: ReportReportGMP = element()
    report_format_param: ReportReportFormatParam | None = wrapped(
        "report_format", element(tag="param"), default=None
    )
    sort_field: ReportReportField = wrapped("sort", element(tag="field"))
    filters: ReportReportFilters = element()
    delta: ReportReportDelta | None = element(default=None)
    scan_run_status: str | None = element(tag="scan_run_status")
    permissions: list[Permission] | None = wrapped(
        "permissions", element(tag="permission", default=None)
    )
    user_tags: UserTags | None = element(default=None)
    scan_result_status: str | None = element(default=None)
    result_count: ReportReportResultCount | None = element(default=None)
    severity: ReportReportFullFiltered | None = element(tag="severity", default=None)
    hosts: ReportReportCount | None = element(tag="hosts", default=None)
    closed_cves: ReportReportCount | None = element(tag="closed_cves", default=None)
    vulns: ReportReportCount | None = element(tag="vulns", default=None)
    os: ReportReportCount | None = element(tag="os", default=None)
    apps: ReportReportCount | None = element(tag="apps", default=None)
    ssl_certs: ReportReportCount | None = element(tag="ssl_certs", default=None)
    task: ReportReportTask | None = element(tag="task", default=None)
    tls_certificates: ReportReportTLSCertificate | None = element(
        tag="tls_certificates", default=None
    )
    timestamp: datetime | None = element(default=None)
    scan_start: datetime | None = element(default=None)
    scan_end: datetime | None = element(default=None)
    timezone: str | None = element(default=None)
    timezone_abbrev: str | None = element(default=None)
    ports: ReportReportPorts | None = element(tag="ports", default=None)
    results: ReportReportResults | None = element(tag="results", default=None)
    errors: ReportReportErrors | None = element(default=None)
    report_format: str | None = element(tag="report_format", default=None)


class Report(BaseXmlModel, search_mode="unordered", tag="report"):
    id: str | None = attr(default=None)
    format_id: str | None = attr(default=None)
    extension: str | None = attr(default=None)
    config_id: str | None = attr(default=None)
    content_type: str | None = attr(default=None)
    type: str | None = attr(default=None)
    owner: Owner = element()
    name: str = element()
    comment: str | None = element(default=None)
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    task: Task = element()
    report_format: ReportFormat | None = element(default=None)
    report: ReportReport = element()


class GetReportResponse(BaseModel):
    report: Report


class GetReportsResponse(BaseModel):
    reports: list[Report]


class ImportReportResponse(BaseModel):
    id: str


class ReportImport(BaseModel):
    report: str
    in_assets: bool | None = None
