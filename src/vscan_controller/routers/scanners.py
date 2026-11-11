# pylint: disable=raise-missing-from
import traceback
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from vscan_controller.gvm_tools.scanners import GVMScanners
from vscan_controller.models.scanners import GetScannerResponse, Scanner
from vscan_controller.routers.auth import authorization
from vscan_controller.routers.response import INTERNAL_SERVER_ERROR, UNAUTHORIZED


class ScannersRouter(APIRouter):
    def __init__(self, gvm_scanners: GVMScanners, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/scanners", tags=["scanners"], dependencies=[Depends(authorization)]
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
            responses=http_responses,
        )

    async def get_scanners(
        self,
        *,
        filter_string: str | None = None,
        trash: bool | None = None,
        details: bool | None = None,
    ) -> dict[str, list[Scanner]]:
        try:
            resp = self.gvm_scanners.get_scanners(
                filter_string=filter_string, trash=trash, details=details
            )
            scanners = resp.findall("./scanner")
            res = []
            for s in scanners:
                res.append(Scanner.from_xml(tostring(s)))
            return {"scanners": res}
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
                "call of adapter or xml conversion of scanners failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e
