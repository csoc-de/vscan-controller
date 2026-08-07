from __future__ import annotations

from datetime import datetime
from typing import Optional, Annotated

from lxml.etree import _Element as Element
from pydantic import BaseModel, Field, computed_field
from pydantic_xml import element, attr, BaseXmlModel, wrapped

from app.models.base import Permission, UserTags, Owner


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
        return (self.column == other.column) and (self.relation == other.relation) and (self.value == other.value)


class ReportReportFiltersDelta(BaseXmlModel, search_mode="unordered", tag="delta"):
    changed: str = element()
    gone: str = element()
    new: str = element()
    same: str = element()


class ReportReportFilters(BaseXmlModel, search_mode="unordered", tag="filters"):
    id: Optional[str] = attr(default=None)
    term: str = element()
    phrase: Optional[str] = element(default=None)
    notes: Optional[int] = element(default=None)
    overrides: Optional[int] = element(default=None)
    result_hosts_only: Optional[int] = element(default=None)
    min_qod: Optional[str] = element(default=None)
    delta: Optional[ReportReportFiltersDelta] = element(default=None)
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
    deprecated: Optional[str] = None
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
    comment: Optional[str] = element(default=None)


class ReportReportTask(BaseXmlModel, search_mode="unordered", tag="task"):
    id: str = attr()
    name: str = element()
    comment: Optional[str] = element(default=None)
    target: ReportReportTaskTarget = element(tag="target")
    progress: int = element()
    user_tags: Optional[UserTags] = element(default=None, tag="user_tags")


class ReportReportPortsPort(BaseXmlModel, search_mode="unordered", tag="port", arbitrary_types_allowed=True):
    host: Annotated[Element, Field(exclude=True)] = element(
        field=Field(exclude=True, default=None))  # field is excluded (fastapi)
    # port: Optional[str] = None
    severity: Optional[float] = element(default=None)
    threat: Optional[str] = element(default=None)

    @computed_field(return_type=Optional[str])
    @property
    def host_name(self):
        return self.host.text

    @host_name.setter
    def host_name(self, name: str):
        self.host.text = name

    @computed_field(return_type=Optional[str])
    @property
    def host_port(self):
        return self.host.tail

    @host_port.setter
    def host_port(self, port: str):
        self.host.tail = port


class ReportReportPorts(BaseXmlModel, search_mode="unordered", tag="ports"):
    start: int = attr()
    max: int = attr()
    count: int = element()
    ports: Optional[list[ReportReportPortsPort]] = element(tag="port", default=None)


class ReportReportResultReport(BaseXmlModel, search_mode="unordered", tag="report"):
    id: str = attr()


class ReportReportAsset(BaseXmlModel, search_mode="unordered", tag="asset"):
    asset_id: str = attr()


class ReportReportResultHost(BaseXmlModel, search_mode="unordered", tag="host"):
    host: str
    asset: ReportReportAsset = element(tag="asset")
    hostname: Optional[str] = element(default=None)


class ReportReportResultNVTSeverity(BaseXmlModel, search_mode="unordered", tag="severity"):
    type: str = attr()
    origin: Optional[str] = element(default=None)
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
    solution: Optional[str] = None
    type: Optional[str] = attr(default=None)


class ReportReportResultNVT(BaseXmlModel, search_mode="unordered", tag="nvt"):
    oid: str = attr()
    type: str = element()
    name: str = element()
    family: str = element()
    cvss_base: float = element()
    severities: ReportReportResultNVTSeverities = element()
    cpe: Optional[str] = element(default=None)
    tags: str = element()
    refs: Optional[list[ReportReportResultNVTReference]] = wrapped("refs", default=None, tag="ref")
    solution: Optional[ReportReportResultNVTSolution] = element(tag="solution")


class ReportReportResultQOD(BaseXmlModel, search_mode="unordered", tag="qod"):
    value: int = element()
    type: Optional[str] = element(default=None)


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
    cve: Optional[str] = element(default=None)


class ReportReportResultDeltaNoteOrOverwriteResult(BaseXmlModel, search_mode="unordered", tag="result"):
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
    user_tags: Optional[UserTags] = element(tag="user_tags", default=None)
    hosts: Optional[str] = element(default=None)
    port: Optional[str] = element(default=None)
    severity: Optional[float] = element(default=None)
    task: Optional[ReportReportResultDeltaNoteTask] = element(default=None)
    end_time: Optional[datetime] = element(default=None)
    result: Optional[ReportReportResultDeltaNoteOrOverwriteResult] = element(default=None)


class ReportReportResultOverwrite(BaseXmlModel, search_mode="unordered", tag="overwrite"):
    id: str = attr()
    permissions: list[Permission] = wrapped("permissions", element(tag="permission"))
    owner: Owner = element(tag="owner")
    nvt: ReportReportResultDeltaNoteNVT = element()
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    user_tags: Optional[UserTags] = element(tag="user_tags", default=None)
    active: bool = element()
    orphan: bool = element()
    text: ReportReportResultDeltaNoteText = element()
    severity: str = element()
    threat: str = element()
    new_severity: str = element()
    new_threat: str = element()
    hosts: Optional[str] = element(default=None)
    port: Optional[str] = element(default=None)
    task: Optional[ReportReportResultDeltaNoteTask] = element(default=None)
    end_time: Optional[datetime] = element(default=None)
    result: Optional[ReportReportResultDeltaNoteOrOverwriteResult] = element(default=None)


class ReportReportResultDelta(BaseXmlModel, search_mode="unordered", tag="delta"):
    result: Optional[ReportReportResult] = element()
    diff: str = element()
    notes: Optional[list[ReportReportResultNote]] = element(tag="note", default=None)
    overwrites: Optional[list[ReportReportResultOverwrite]] = element(tag="overwrite", default=None)


class ReportReportResultDetectionResultDetail(BaseXmlModel, search_mode="unordered", tag="detail"):
    name: str = element()
    value: str = element()


class ReportReportResultDetectionResult(BaseXmlModel, search_mode="unordered", tag="result"):
    id: str = attr()
    details: Optional[list[ReportReportResultDetectionResultDetail]] = wrapped(path="details", tag="detail",
                                                                               default=None)


class ReportReportResultDetection(BaseXmlModel, search_mode="unordered", tag="detection"):
    result: ReportReportResultDetectionResult = element()


class ReportReportResultTicket(BaseXmlModel, search_mode="unordered", tag="ticket"):
    id: str = attr()


class ReportReportResult(BaseXmlModel, search_mode="unordered", tag="result"):
    id: str = attr()
    name: str = element()
    owner: Owner = element(tag="owner")
    modification_time: datetime = element()
    comment: Optional[str] = element(default=None)
    creation_time: datetime = element()
    detection: Optional[ReportReportResultDetection] = element(default=None)
    host: ReportReportResultHost = element()
    port: str = element()
    nvt: ReportReportResultNVT = element()
    report: Optional[ReportReportResultReport] = element(tag="report", default=None)
    task: Optional[ReportReportTask] = element(tag="task", default=None)
    path: Optional[str] = element(default=None)
    scan_nvt_version: datetime = element()
    threat: str = element()
    severity: float = element()
    qod: ReportReportResultQOD = element()
    description: Optional[str] = element(default=None)
    original_threat: Optional[str] = element(default=None)
    original_severity: Optional[float] = element(default=None)
    compliance: Optional[str] = element(default=None)
    # delta: Optional[ReportReportResultDelta] = element(default=None)
    notes: Optional[list[ReportReportResultNote]] = element(tag="note", default=None)
    overwrites: Optional[list[ReportReportResultOverwrite]] = element(tag="overwrite", default=None)
    tickets: Optional[ReportReportResultTicket] = element(tag="tickets", default=None)
    user_tags: Optional[UserTags] = element(tag="user_tags", default=None)


class ReportReportResults(BaseXmlModel, search_mode="unordered", tag="results"):
    start: int = attr()
    max: int = attr()
    results: Optional[list[ReportReportResult]] = element(tag="result", default=None)


class ReportReportHosts(BaseXmlModel, search_mode="unordered", tag="hosts"):
    start: Optional[int] = attr(default=None)
    max: Optional[int] = attr(default=None)
    count: Optional[int] = attr(default=None)


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


class ReportReportTLSCertificateCertificate(BaseXmlModel, search_mode="unordered", tag="certificate"):
    format: str = attr()


class ReportReportTLSCertificateHost(BaseXmlModel, search_mode="unordered", tag="host"):
    ip: str = element()
    hostname: str = element()


class ReportReportTLSCertificate(BaseXmlModel, search_mode="unordered", tag="tls_certificate"):
    name: Optional[str] = element(default=None)
    certificate: Optional[ReportReportTLSCertificateCertificate] = element(tag="certificate", default=None)
    sha256_fingerprint: Optional[str] = element(default=None)
    md5_fingerprint: Optional[str] = element(default=None)
    valid: Optional[bool] = element(default=None)
    activation_time: Optional[datetime] = element(default=None)
    expiration_time: Optional[datetime] = element(default=None)
    subject_dn: Optional[str] = element(default=None)
    issuer_dn: Optional[str] = element(default=None)
    serial: Optional[str] = element(default=None)
    host: Optional[ReportReportTLSCertificateHost] = element(default=None)
    ports: Optional[list[str]] = wrapped("ports", element(tag="port"), default=None)


class ReportReportErrorNVT(BaseXmlModel, search_mode="unordered", tag="nvt"):
    oid: str = attr()
    name: str = element()
    type: str = element()
    cvss_base: str = element()


class ReportReportError(BaseXmlModel, search_mode="unordered", tag="error"):
    host: ReportReportResultHost = element(tag="host")
    port: str = element()
    description: str = element()
    nvt: ReportReportErrorNVT = element()
    scan_nvt_version: str = element()
    severity: float = element()


class ReportReportErrors(BaseXmlModel, search_mode="unordered", tag="errors"):
    count: int = element()
    errors: Optional[list[ReportReportError]] = element(tag="error", default=None)


class ReportReport(BaseXmlModel, search_mode="unordered", tag="report"):
    id: str = attr()
    type: Optional[str] = attr(default=None)
    gmp: ReportReportGMP = element()
    report_format_param: Optional[ReportReportFormatParam] = wrapped(
        "report_format",
        element(tag="param"),
        default=None
    )
    sort_field: ReportReportField = wrapped("sort", element(tag="field"))
    filters: ReportReportFilters = element()
    delta: Optional[ReportReportDelta] = element(default=None)
    scan_run_status: Optional[str] = element(tag="scan_run_status")
    permissions: Optional[list[Permission]] = wrapped("permissions",
                                                      element(tag="permission", default=None))
    user_tags: Optional[UserTags] = element(default=None)
    scan_result_status: Optional[str] = element(default=None)
    result_count: Optional[ReportReportResultCount] = element(default=None)
    severity: Optional[ReportReportFullFiltered] = element(tag="severity", default=None)
    hosts: Optional[ReportReportCount] = element(tag="hosts", default=None)
    closed_cves: Optional[ReportReportCount] = element(tag="closed_cves", default=None)
    vulns: Optional[ReportReportCount] = element(tag="vulns", default=None)
    os: Optional[ReportReportCount] = element(tag="os", default=None)
    apps: Optional[ReportReportCount] = element(tag="apps", default=None)
    ssl_certs: Optional[ReportReportCount] = element(tag="ssl_certs", default=None)
    task: Optional[ReportReportTask] = element(tag="task", default=None)
    tls_certificates: Optional[ReportReportTLSCertificate] = element(tag="tls_certificates", default=None)
    timestamp: Optional[datetime] = element(default=None)
    scan_start: Optional[datetime] = element(default=None)
    scan_end: Optional[datetime] = element(default=None)
    timezone: Optional[str] = element(default=None)
    timezone_abbrev: Optional[str] = element(default=None)
    ports: Optional[ReportReportPorts] = element(tag="ports", default=None)
    results: Optional[ReportReportResults] = element(tag="results", default=None)
    errors: Optional[ReportReportErrors] = element(default=None)
    report_format: Optional[str] = element(tag="report_format", default=None)


class Report(BaseXmlModel, search_mode="unordered", tag="report"):
    id: Optional[str] = attr(default=None)
    format_id: Optional[str] = attr(default=None)
    extension: Optional[str] = attr(default=None)
    config_id: Optional[str] = attr(default=None)
    content_type: Optional[str] = attr(default=None)
    type: Optional[str] = attr(default=None)
    owner: Owner = element()
    name: str = element()
    comment: Optional[str] = element(default=None)
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    task: Task = element()
    report_format: Optional[ReportFormat] = element(default=None)
    report: ReportReport = element()


class GetReportResponse(BaseModel):
    report: Report


class GetReportsResponse(BaseModel):
    reports: list[Report]


class ImportReportResponse(BaseModel):
    id: str


class ReportImport(BaseModel):
    report: str
    in_assets: Optional[bool] = None
