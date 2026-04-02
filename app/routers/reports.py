# pylint: disable=raise-missing-from
from typing import Dict, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from app.gvm_tools.reports import GVMReports
from app.models.reports import Report, GetReportsResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR


class ReportsRouter(APIRouter):
    def __init__(self, gvm_reports: GVMReports, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/reports",
            tags=["reports"],
            dependencies=[Depends(authorization)]
        )
        self.gvm_reports = gvm_reports
        self._log = log

        # GET Port Lists
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
