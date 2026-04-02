from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic_xml import element, attr, BaseXmlModel, wrapped

from app.models.base import Permission, UserTags, ResultCount, Owner


class Task(BaseXmlModel, tag="task"):
    id: str = attr()
    name: str = element()


class ReportFormat(BaseXmlModel, tag="report_format"):
    id: str = attr()
    name: str = element()


class ReportReportGMP(BaseXmlModel, tag="gmp"):
    version: str = element()


class ReportReportFormatParam(BaseXmlModel, tag="param"):
    name: str = element()
    value: str = element()


class ReportReportFieldOrder(BaseXmlModel, tag="order"):
    order: str = element()


class ReportReportField(BaseXmlModel, tag="field"):
    text: str
    order: ReportReportFieldOrder = element()


class ReportReportFilterKeyword(BaseXmlModel, tag="keyword"):
    column: str = element()
    relation: str = element()
    value: str = element()


class ReportReportFiltersDelta(BaseXmlModel, tag="delta"):
    changed: str = element()
    gone: str = element()
    new: str = element()
    same: str = element()


class ReportReportFilters(BaseXmlModel, tag="filters"):
    term: str = element()
    phrase: Optional[str] = element(default=None)
    notes: Optional[int] = element(default=None)
    overrides: Optional[int] = element(default=None)
    result_hosts_only: Optional[int] = element(default=None)
    min_qod: Optional[str] = element(default=None)
    delta: Optional[ReportReportFiltersDelta] = element(default=None)
    filter: list[str] = element()
    keywords: list[ReportReportFilterKeyword] = wrapped("keywords", element(tag="keyword"))


class ReportReportDeltaReport(BaseXmlModel, tag="report"):
    id: str = attr()
    scan_run_status: str = element()
    timestamp: datetime = element()
    scan_start: datetime = element()
    scan_end: datetime = element()


class ReportReportDelta(BaseXmlModel, tag="delta"):
    report: ReportReportDeltaReport = element()


class ReportReportFullFiltered(BaseXmlModel):
    full: int = element()
    filtered: int = element()


class ReportReportResultCount(ResultCount, tag="result_count"):
    full: int = element()
    filtered: int = element()


class ReportReportTaskTarget(BaseXmlModel, tag="target"):
    id: str = attr()
    trash: bool = element()
    name: str = element()
    comment: str = element()


class ReportReportTask(BaseXmlModel, tag="task"):
    id: str = attr()
    name: str = element()
    target: ReportReportTaskTarget = element(tag="target")
    progress: str = element()
    user_tags: Optional[UserTags] = element(tag="user_tags")


class ReportReportPortsPort(BaseXmlModel, tag="port"):
    host: str = element()
    severity: str = element()
    threat: str = element()


class ReportReportPorts(BaseXmlModel, tag="ports"):
    start: int = attr()
    max: int = attr()
    ports: list[ReportReportPortsPort] = element(tag="port")


class ReportReportResultReport(BaseXmlModel, tag="report"):
    id: str = attr()


class ReportReportAsset(BaseXmlModel, tag="asset"):
    asset_id: str = attr()


class ReportReportResultHost(BaseXmlModel, tag="host"):
    hostname: Optional[str] = element(default=None)
    asset: ReportReportAsset = element(tag="asset")


class ReportReportResultNVTSeverity(BaseXmlModel, tag="severity"):
    type: str = attr()
    origin: str = element()
    date: datetime = element()
    score: float = element()
    value: str = element()


class ReportReportResultNVTSeverities(BaseXmlModel, tag="severities"):
    score: str = element()
    severities: list[ReportReportResultNVTSeverity] = element(tag="severity")


class ReportReportResultNVTReference(BaseXmlModel, tag="ref"):
    id: str = attr()
    type: str = attr()


class ReportReportResultNVT(BaseXmlModel, tag="nvt"):
    oid: str = attr()
    name: str = element()
    type: str = element()
    cvss_base: str = element()
    severities: ReportReportResultNVTSeverities = element()
    cpe: str = element()
    tags: str = element()
    refs: list[ReportReportResultNVTReference] = element(tag="ref")


class ReportReportResultQOD(BaseXmlModel, tag="qod"):
    value: int = element()
    type: str = element()


class ReportReportResultDeltaNoteNVT(BaseXmlModel, tag="nvt"):
    oid: str = attr()
    name: str = element()
    type: str = element()


class ReportReportResultDeltaNoteText(BaseXmlModel, tag="text"):
    excerpt: bool = attr()


class ReportReportResultDeltaNoteTask(BaseXmlModel, tag="task"):
    id: str = attr()


class ReportReportResultDeltaNoteResultNVT(BaseXmlModel, tag="nvt"):
    oid: str = attr()
    name: str = element()
    type: str = element()
    cvss_base: str = element()
    severities: ReportReportResultNVTSeverities = element()
    cve: Optional[str] = element(default=None)


class ReportReportResultDeltaNoteOrOverwriteResult(BaseXmlModel, tag="result"):
    id: str = attr()
    host: ReportReportResultHost = element()
    port: str = element()
    nvt: ReportReportResultDeltaNoteResultNVT = element()
    severity: str = element()
    threat: str = element()
    qod: ReportReportResultQOD = element()
    description: str = element()


class ReportReportResultNote(BaseXmlModel, tag="note"):
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


class ReportReportResultOverwrite(BaseXmlModel, tag="overwrite"):
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


class ReportReportResultDelta(BaseXmlModel, tag="delta"):
    result: Optional[ReportReportResult] = element()
    diff: str = element()
    notes: Optional[list[ReportReportResultNote]] = element(tag="note", default=None)
    overwrites: Optional[list[ReportReportResultOverwrite]] = element(tag="overwrite", default=None)


class ReportReportResultDetectionResultDetail(BaseXmlModel, tag="detail"):
    name: str = element()
    value: str = element()


class ReportReportResultDetectionResult(BaseXmlModel, tag="result"):
    id: str = attr()
    details: Optional[list[ReportReportResultDetectionResultDetail]] = element(tag="detail", default=None)


class ReportReportResultDetection(BaseXmlModel, tag="detection"):
    result: ReportReportResultDetection = element()


class ReportReportResultTicket(BaseXmlModel, tag="ticket"):
    id: str = attr()


class ReportReportResult(BaseXmlModel, tag="result"):
    id: str = attr()
    name: str = element()
    owner: Owner = element(tag="owner")
    comment: str = element()
    creation_time: datetime = element()
    modification_time: datetime = element()
    user_tags: Optional[UserTags] = element(tag="user_tags", default=None)
    report: Optional[ReportReportResultReport] = element(tag="report", default=None)
    task: Optional[ReportReportTask] = element(tag="task", default=None)
    host: ReportReportResultHost = element()
    port: str = element()
    path: Optional[str] = element()
    nvt: ReportReportResultNVT = element()
    scan_nvt_version: str = element()
    threat: str = element()
    severity: str = element()
    qod: ReportReportResultQOD = element()
    original_threat: Optional[str] = element(default=None)
    original_severity: Optional[str] = element(default=None)
    description: str = element()
    delta: Optional[ReportReportResultDelta] = element(default=None)
    detection: Optional[ReportReportResultDetection] = element(default=None)
    notes: Optional[list[ReportReportResultNote]] = element(tag="note", default=None)
    overwrites: Optional[list[ReportReportResultOverwrite]] = element(tag="overwrite", default=None)
    tickets: Optional[ReportReportResultTicket] = element(tag="tickets", default=None)


class ReportReportResults(BaseXmlModel, tag="results"):
    start: int = attr()
    max: int = attr()
    results: list[ReportReportResult] = element(tag="result")


class ReportReportHosts(BaseXmlModel, tag="hosts"):
    start: Optional[int] = attr(default=None)
    max: Optional[int] = attr(default=None)
    count: Optional[int] = attr(default=None)


class ReportReportCount(BaseXmlModel):
    count: int = element()


class ReportReportHostResultSeverity(BaseXmlModel, tag="page"):
    text: str
    page: int = element()


class ReportReportHostResultCount(BaseXmlModel, tag="result_count"):
    page: int = element()
    hole: ReportReportHostResultSeverity = element(tag="hole")
    warning: ReportReportHostResultSeverity = element(tag="warning")
    info: ReportReportHostResultSeverity = element(tag="info")
    log: ReportReportHostResultSeverity = element(tag="log")
    false_positive: ReportReportHostResultSeverity = element(tag="false_positive")


class ReportReportHostDetailSource(BaseXmlModel, tag="source"):
    type: str = element()
    name: str = element()
    description: str = element()


class ReportReportHostDetail(BaseXmlModel, tag="detail"):
    name: str = element()
    value: str = element()
    source: ReportReportHostDetailSource = element(tag="source")
    extra: str = element()


class ReportReportHost(BaseXmlModel, tag="host"):
    ip: str = element()
    asset: ReportReportAsset = element()
    start: datetime = element()
    end: datetime = element()
    port_count: ReportReportHostResultSeverity = element(tag="port_count")
    result_count: ReportReportHostResultCount = element(tag="result_count")
    details: list[ReportReportHostDetail] = element(tag="detail")


class ReportReportTLSCertificateCertificate(BaseXmlModel, tag="certificate"):
    format: str = attr()


class ReportReportTLSCertificateHost(BaseXmlModel, tag="host"):
    ip: str = element()
    hostname: str = element()


class ReportReportTLSCertificate(BaseXmlModel, tag="tls_certificate"):
    name: str = element()
    certificate: ReportReportTLSCertificateCertificate = element(tag="certificate")
    sha256_fingerprint: str = element()
    md5_fingerprint: str = element()
    valid: bool = element()
    activation_time: datetime = element()
    expiration_time: datetime = element()
    subject_dn: str = element()
    issuer_dn: str = element()
    serial: str = element()
    host: ReportReportTLSCertificateHost = element()
    ports: list[str] = wrapped("ports", element(tag="port"))


class ReportReportErrorNVT(BaseXmlModel, tag="nvt"):
    oid: str = attr()
    name: str = element()
    type: str = element()
    cvss_base: str = element()


class ReportReportError(BaseXmlModel, tag="error"):
    host: ReportReportResultHost = element(tag="host")
    port: str = element()
    description: str = element()
    nvt: ReportReportErrorNVT = element()
    scan_nvt_version: str = element()
    severity: float = element()


class ReportReportErrors(BaseXmlModel, tag="errors"):
    count: int = element()
    errors: list[ReportReportError] = element(tag="error")


class ReportReport(BaseXmlModel, tag="report"):
    id: str = attr()
    type: str = attr()
    gmp: ReportReportGMP = element()
    report_format_param: ReportReportFormatParam = wrapped("report_format", element(tag="param"))
    sort_field: ReportReportField = wrapped("sort", element(tag="field"))
    filters: ReportReportFilters = element()
    delta: Optional[ReportReportDelta] = element(default=None)
    timezone: Optional[str] = element(default=None)
    timezone_abbrev: Optional[str] = element(default=None)
    permissions: Optional[list[Permission]] = wrapped("permissions",
                                                      element(tag="permission", default=None))
    user_tags: Optional[UserTags] = element(default=None)
    scan_result_status: Optional[str] = element(default=None)
    result_count: Optional[ReportReportResultCount] = element(default=None)
    severity: Optional[ReportReportFullFiltered] = element(tag="severity", default=None)
    task: Optional[ReportReportTask] = element(tag="task", default=None)
    ports: Optional[list[ReportReportPortsPort]] = element(tag="port", default=None)
    results: Optional[ReportReportResults] = element(tag="results", default=None)
    closed_cves: Optional[ReportReportCount] = element(tag="closed_cves", default=None)
    vulns: Optional[ReportReportCount] = element(tag="vulns", default=None)
    os: Optional[ReportReportCount] = element(tag="os", default=None)
    apps: Optional[ReportReportCount] = element(tag="apps", default=None)
    ssl_certs: Optional[ReportReportCount] = element(tag="ssl_certs", default=None)
    hosts: Optional[list[ReportReportHost]] = element(tag="host", default=None)
    tls_certificates: Optional[ReportReportTLSCertificate] = element(tag="tls_certificates", default=None)
    timestamp: Optional[datetime] = element(default=None)
    scan_start: Optional[datetime] = element(default=None)
    scan_end: Optional[datetime] = element(default=None)
    errors: Optional[ReportReportErrors] = element(default=None)


class Report(BaseXmlModel, tag="report"):
    id: str = attr()
    format_id: str = attr()
    extension: str = attr()
    content_type: str = attr()
    type: str = attr()
    owner: Owner = element()
    name: str = element()
    comment: str = element()
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    un_use: bool = element()
    task: Task = element()
    report_format: ReportFormat = element()


class GetReportResponse(BaseModel):
    reports: Report


class GetReportsResponse(BaseModel):
    reports: list[Report]


class ImportReportResponse(BaseModel):
    id: str


class ReportImport(BaseModel):
    report: str
    in_assets: Optional[bool] = None
