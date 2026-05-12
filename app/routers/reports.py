# pylint: disable=raise-missing-from
from typing import Dict, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from app.gvm_tools.reports import GVMReports
from app.models.reports import Report, GetReportsResponse, GetReportResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR, NOT_FOUND


class ReportsRouter(APIRouter):
    def __init__(self, gvm_reports: GVMReports, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/reports",
            tags=["reports"],
            dependencies=[Depends(authorization)]
        )
        self.gvm_reports = gvm_reports
        self._log = log

        # GET Report
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.get_report,
            methods=["GET"],
            response_model=GetReportResponse,
            responses=http_responses
        )

        # GET Reports
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_reports,
            methods=["GET"],
            response_model=GetReportsResponse,
            responses=http_responses
        )

        # POST Import Report
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "/import",
            self.import_report,
            methods=["POST"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

    async def get_report(self, uuid: str) -> Dict[str, Report]:
        try:
            resp = self.gvm_reports.get_report(uuid)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="report not found"
                    )
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )
        report = resp.findall("./report")
        print(tostring(report[0]))
        if len(report) > 1:
            self._log.error("multiple reports with same uuid found")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="multiple reports with same uuid found"
            )
        return {"report": Report.from_xml(tostring(report[0]))}

    async def get_reports(
            self,
            *,
            filter_string: Optional[str] = None,
            filter_id: Optional[str] = None,
            note_details: Optional[bool] = None,
            override_details: Optional[bool] = None,
            ignore_pagination: Optional[bool] = None,
            details: Optional[bool] = None,
    ) -> Dict[str, list[Report]]:
        try:
            resp = self.gvm_reports.get_reports(filter_string=filter_string, filter_id=filter_id,
                                                note_details=note_details, override_details=override_details,
                                                ignore_pagination=ignore_pagination, details=details)
        except GvmResponseError as e:
            match e.status:
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )
        reports = resp.findall("./report")
        res = []
        for r in reports:
            print(tostring(r))
            res.append(Report.from_xml(tostring(r)))
        return {"reports": res}

    async def import_report(
            self,
            report: str,
            task_id: str,
            *,
            in_assets: Optional[bool] = None,
    ):
        try:
            resp = self.gvm_reports.import_report(report, task_id, in_assets=in_assets)
            print(resp)
        except GvmResponseError as e:
            match e.status:
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )
