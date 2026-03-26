from typing import Dict, List, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from structlog.stdlib import BoundLogger

from app.gvm_tools.gvm import status_response_code_ok, get_status_response_code
from app.gvm_tools.scanners import GVMScanners
from app.models.scanners import Scanner, GetScannerResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR


class ScannersRouter(APIRouter):
    def __init__(self, gvm_scanners: GVMScanners, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/scanners",
            tags=["scanners"],
            dependencies=[Depends(authorization)]
        )
        self.gvm_scanners = gvm_scanners
        self._log = log

        # GET Port Lists
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_scanners,
            methods=["GET"],
            response_model=GetScannerResponse,
            responses=http_responses
        )

    async def get_scanners(
            self,
            *,
            filter_string: Optional[str] = None,
            trash: Optional[bool] = None,
            details: Optional[bool] = None,
    ) -> Dict[str, List[Scanner]]:
        resp = self.gvm_scanners.get_scanners(filter_string=filter_string, trash=trash, details=details)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
        scanners = resp.findall("./scanner")
        res = []
        for s in scanners:
            res.append(Scanner.from_xml(tostring(s)))
        return {"scanners": res}
