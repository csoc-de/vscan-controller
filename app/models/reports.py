from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic_xml import element, attr, BaseXmlModel, wrapped


class Owner(BaseXmlModel, tag="owner"):
    name: str = element()


class Task(BaseXmlModel, tag="task"):
    id: str = attr()
    name: str = element()


class ReportReportGMP(BaseXmlModel, tag="gmp"):
    version: str = element()


class ReportReportField(BaseXmlModel, tag="field"):
    text: str
    order: Optional[str] = element(tag="order", default=None)


class ReportReportFilterKeyword(BaseXmlModel, tag="keyword"):
    column: str = element()
    relation: str = element()
    value: str = element()


class ReportReportFilters(BaseXmlModel, tag="filters"):
    id: Optional[str] = attr(default=None)
    term: str = element()
    filter: list[str] = element()
    keywords: list[ReportReportFilterKeyword] = wrapped("keywords", element(tag="keyword"), default=[])


class ReportReportFullFiltered(BaseXmlModel):
    full: float = element()
    filtered: float = element()


class ReportReportResultCountDetail(BaseXmlModel):
    full: int = element()
    filtered: int = element()


class ReportReportResultCount(BaseXmlModel, tag="result_count"):
    text: Optional[str] = None
    full: Optional[int] = element(default=None)
    filtered: Optional[int] = element(default=None)
    critical: Optional[ReportReportResultCountDetail] = element(default=None)
    high: Optional[ReportReportResultCountDetail] = element(default=None)
    medium: Optional[ReportReportResultCountDetail] = element(default=None)
    low: Optional[ReportReportResultCountDetail] = element(default=None)
    hole: Optional[ReportReportResultCountDetail] = element(default=None)
    info: Optional[ReportReportResultCountDetail] = element(default=None)
    log: Optional[ReportReportResultCountDetail] = element(default=None)
    warning: Optional[ReportReportResultCountDetail] = element(default=None)
    false_positive: Optional[ReportReportResultCountDetail] = element(default=None)


class ReportReportTaskTarget(BaseXmlModel, tag="target"):
    id: str = attr()
    trash: int = element()
    name: str = element()
    comment: Optional[str] = element(default=None)


class ReportReportTask(BaseXmlModel, tag="task"):
    id: str = attr()
    name: str = element()
    comment: Optional[str] = element(default=None)
    target: Optional[ReportReportTaskTarget] = element(tag="target", default=None)
    progress: Optional[int] = element(default=None)


class ReportReportPortsPort(BaseXmlModel, tag="port", search_mode="unordered"):
    text: Optional[str] = element(tag="text", default=None)
    host: str = element()
    severity: float = element()
    threat: str = element()


class ReportReportPorts(BaseXmlModel, tag="ports"):
    count: int = element(tag="count", default=0)
    ports: list[ReportReportPortsPort] = element(tag="port", default=[])


class ReportReportAsset(BaseXmlModel, tag="asset"):
    asset_id: str = attr()


class ReportReportResultHost(BaseXmlModel, tag="host"):
    ip: Optional[str] = None
    asset: ReportReportAsset = element(tag="asset")
    hostname: Optional[str] = element(default=None)


class ReportReportResultNVTSeverity(BaseXmlModel, tag="severity"):
    type: str = attr()
    origin: Optional[str] = element(default=None)
    date: datetime = element()
    score: float = element()
    value: str = element()


class ReportReportResultNVTSeverities(BaseXmlModel, tag="severities"):
    score: float = attr()
    severity: list[ReportReportResultNVTSeverity] = element(tag="severity", default=[])


class ReportReportResultNVTReference(BaseXmlModel, tag="ref"):
    id: str = attr()
    type: str = attr()


class ReportReportResultNVT(BaseXmlModel, tag="nvt"):
    oid: str = attr()
    type: str = element()
    name: str = element()
    family: Optional[str] = element(default=None)
    cvss_base: float = element()
    severities: ReportReportResultNVTSeverities = element()
    tags: str = element()
    solution: Optional[str] = element(default=None)
    refs: list[ReportReportResultNVTReference] = wrapped("refs", element(tag="ref"), default=[])


class ReportReportResultQOD(BaseXmlModel, tag="qod"):
    value: int = element()
    type: Optional[str] = element(default=None)


class ReportReportResultDetectionResultDetail(BaseXmlModel, tag="detail"):
    name: str = element()
    value: str = element()


class ReportReportResultDetectionResult(BaseXmlModel, tag="result"):
    id: str = attr()
    details: list[ReportReportResultDetectionResultDetail] = wrapped("details", element(tag="detail"), default=[])


class ReportReportResultDetection(BaseXmlModel, tag="detection"):
    result: ReportReportResultDetectionResult = element()


class ReportReportResult(BaseXmlModel, tag="result", search_mode="unordered"):
    id: str = attr()
    name: str = element()
    owner: Owner = element(tag="owner")
    modification_time: datetime = element()
    comment: Optional[str] = element(default=None)
    creation_time: datetime = element()
    host: ReportReportResultHost = element()
    port: str = element()
    nvt: ReportReportResultNVT = element()
    scan_nvt_version: str = element()
    threat: str = element()
    severity: float = element()
    qod: ReportReportResultQOD = element()
    description: str = element()
    original_threat: Optional[str] = element(default=None)
    original_severity: Optional[float] = element(default=None)
    compliance: Optional[str] = element(default=None)
    detection: Optional[ReportReportResultDetection] = element(default=None)


class ReportReportResults(BaseXmlModel, tag="results"):
    start: int = attr()
    max: int = attr()
    results: list[ReportReportResult] = element(tag="result", default=[])


class ReportReportHosts(BaseXmlModel, tag="hosts"):
    count: int = element(tag="count")


class ReportReportHostResultSeverity(BaseXmlModel, tag="page"):
    page: int = element()


class ReportReportHostResultCount(BaseXmlModel, tag="result_count"):
    page: int = element()
    critical: Optional[ReportReportHostResultSeverity] = element(tag="critical", default=None)
    hole: Optional[ReportReportHostResultSeverity] = element(tag="hole", default=None)
    high: Optional[ReportReportHostResultSeverity] = element(tag="high", default=None)
    warning: Optional[ReportReportHostResultSeverity] = element(tag="warning", default=None)
    medium: Optional[ReportReportHostResultSeverity] = element(tag="medium", default=None)
    info: Optional[ReportReportHostResultSeverity] = element(tag="info", default=None)
    low: Optional[ReportReportHostResultSeverity] = element(tag="low", default=None)
    log: Optional[ReportReportHostResultSeverity] = element(tag="log", default=None)
    false_positive: Optional[ReportReportHostResultSeverity] = element(tag="false_positive", default=None)


class ReportReportHostDetailSource(BaseXmlModel, tag="source"):
    type: str = element()
    name: str = element()
    description: Optional[str] = element(default=None)


class ReportReportHostDetail(BaseXmlModel, tag="detail"):
    name: str = element()
    value: str = element()
    source: ReportReportHostDetailSource = element(tag="source")
    extra: Optional[str] = element(default=None)


class ReportReportHost(BaseXmlModel, tag="host"):
    ip: str = element()
    asset: ReportReportAsset = element()
    start: datetime = element()
    end: datetime = element()
    port_count: ReportReportHostResultSeverity = element(tag="port_count")
    result_count: ReportReportHostResultCount = element(tag="result_count")
    details: list[ReportReportHostDetail] = element(tag="detail", default=[])


class ReportReportTLSCertificateCertificate(BaseXmlModel, tag="certificate"):
    format: str = attr()


class ReportReportTLSCertificateHost(BaseXmlModel, tag="host"):
    ip: str = element()
    hostname: str = element()


class ReportReportTLSCertificate(BaseXmlModel, tag="tls_certificates"):
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
    ports: Optional[list[str]] = wrapped("ports", element(tag="port", default=None), default=None)


class ReportReportErrors(BaseXmlModel, tag="errors"):
    count: int = element()


class ReportReport(BaseXmlModel, tag="report", search_mode="unordered"):
    id: str = attr()
    gmp: ReportReportGMP = element()
    sort_field: ReportReportField = wrapped("sort", element(tag="field"))
    filters: ReportReportFilters = element()
    scan_run_status: Optional[str] = element(tag="scan_run_status", default=None)
    hosts: Optional[ReportReportHosts] = element(tag="hosts", default=None)
    closed_cves: Optional[ReportReportHosts] = element(tag="closed_cves", default=None)
    vulns: Optional[ReportReportHosts] = element(tag="vulns", default=None)
    os: Optional[ReportReportHosts] = element(tag="os", default=None)
    apps: Optional[ReportReportHosts] = element(tag="apps", default=None)
    ssl_certs: Optional[ReportReportHosts] = element(tag="ssl_certs", default=None)
    task: Optional[ReportReportTask] = element(tag="task", default=None)
    timestamp: Optional[datetime] = element(default=None)
    scan_start: Optional[datetime] = element(default=None)
    timezone: Optional[str] = element(default=None)
    timezone_abbrev: Optional[str] = element(default=None)
    ports: Optional[ReportReportPorts] = element(tag="ports", default=None)
    results: Optional[ReportReportResults] = element(tag="results", default=None)
    result_count: Optional[ReportReportResultCount] = element(tag="result_count", default=None)
    severity: Optional[ReportReportFullFiltered] = element(tag="severity", default=None)
    host: Optional[ReportReportHost] = element(tag="host", default=None)
    tls_certificates: Optional[ReportReportTLSCertificate] = element(tag="tls_certificates", default=None)
    scan_end: Optional[datetime] = element(default=None)
    errors: Optional[ReportReportErrors] = element(default=None)


class Report(BaseXmlModel, tag="report", search_mode="unordered"):
    id: str = attr()
    owner: Owner = element()
    name: str = element()
    comment: Optional[str] = element(default=None)
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    task: Task = element()
    inner_report: ReportReport = element(tag="report")


class GetReportResponse(BaseModel):
    report: Report


class GetReportsResponse(BaseModel):
    reports: list[Report]


class ImportReportResponse(BaseModel):
    id: str


class ReportImport(BaseModel):
    report: str
    in_assets: Optional[bool] = None
