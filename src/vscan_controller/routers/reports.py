# pylint: disable=raise-missing-from
import traceback
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from vscan_controller.gvm_tools.reports import GVMReports
from vscan_controller.models.reports import GetReportResponse, GetReportsResponse, Report
from vscan_controller.routers.auth import authorization
from vscan_controller.routers.response import INTERNAL_SERVER_ERROR, NOT_FOUND, UNAUTHORIZED


class ReportsRouter(APIRouter):
    def __init__(self, gvm_reports: GVMReports, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/reports", tags=["reports"], dependencies=[Depends(authorization)]
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
            responses=http_responses,
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
            responses=http_responses,
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

    async def get_report(self, uuid: str) -> dict[str, Report]:
        try:
            resp = self.gvm_reports.get_report(uuid)
            report = resp.findall("./report")
            if len(report) > 1:
                self._log.error("multiple reports with same uuid found")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="multiple reports with same uuid found",
                )
            return {"report": Report.from_xml(tostring(report[0]))}
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="report not found"
                    ) from e
                case _:
                    self._log.error(
                        "call of adapter failed",
                        error=e,
                        status_code=e.status,
                        traceback=traceback.format_exc(),
                    )
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="internal server error",
                    ) from e
        except Exception as e:
            self._log.error(
                "call of adapter or xml conversion of report failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def get_reports(
        self,
        *,
        filter_string: str | None = None,
        filter_id: str | None = None,
        note_details: bool | None = None,
        override_details: bool | None = None,
        ignore_pagination: bool | None = None,
        details: bool | None = None,
    ) -> dict[str, list[Report]]:
        try:
            resp = self.gvm_reports.get_reports(
                filter_string=filter_string,
                filter_id=filter_id,
                note_details=note_details,
                override_details=override_details,
                ignore_pagination=ignore_pagination,
                details=details,
            )
            reports = resp.findall("./report")
            res = []
            for r in reports:
                res.append(Report.from_xml(tostring(r)))
            return {"reports": res}
        except GvmResponseError as e:
            match e.status:
                case _:
                    self._log.error(
                        "call of adapter failed",
                        error=e,
                        status_code=e.status,
                        traceback=traceback.format_exc(),
                    )
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="internal server error",
                    ) from e
        except Exception as e:
            self._log.error(
                "call of adapter or xml conversion of reports failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def import_report(
        self,
        report: str,
        task_id: str,
        *,
        in_assets: bool | None = None,
    ):
        try:
            _ = self.gvm_reports.import_report(report, task_id, in_assets=in_assets)
        except GvmResponseError as e:
            match e.status:
                case _:
                    self._log.error(
                        "call of adapter failed",
                        error=e,
                        status_code=e.status,
                        traceback=traceback.format_exc(),
                    )
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="internal server error",
                    ) from e
        except Exception as e:
            self._log.error("import failed", error=e, traceback=traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e
