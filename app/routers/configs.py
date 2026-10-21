# pylint: disable=raise-missing-from
import traceback
from typing import Annotated
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, File, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from app.gvm_tools.configs import GVMConfigs
from app.models.configs import (
    Config,
    GetConfigsResponse,
    ImportConfigResponse,
)
from app.routers.auth import authorization
from app.routers.response import INTERNAL_SERVER_ERROR, UNAUTHORIZED


class ConfigsRouter(APIRouter):
    def __init__(self, gvm_configs: GVMConfigs, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/configs",
            tags=["configs"],
            dependencies=[Depends(authorization)],
        )
        self.gvm_configs = gvm_configs
        self._log = log

        # GET Scan Configs
        self.add_api_route(
            "",
            self.get_configs,
            methods=["GET"],
            response_model=GetConfigsResponse,
            responses={**UNAUTHORIZED, **INTERNAL_SERVER_ERROR},
        )

        # POST Import Scan Config
        self.add_api_route(
            "/import",
            self.import_scan_config,
            methods=["POST"],
            response_model=ImportConfigResponse,
            responses={**UNAUTHORIZED, **INTERNAL_SERVER_ERROR},
        )

    async def get_configs(
        self,
        *,
        filter_string: str | None = None,
        trash: bool | None = None,
        details: bool | None = None,
        families: bool | None = None,
        preferences: bool | None = None,
        tasks: bool | None = None,
    ) -> GetConfigsResponse:
        try:
            resp = self.gvm_configs.get_configs(
                filter_string=filter_string,
                trash=trash,
                details=details,
                families=families,
                preferences=preferences,
                tasks=tasks,
            )
            configs = resp.findall("./config")
            res = []
            for r in configs:
                res.append(Config.from_xml(tostring(r)))
            return {"configs": res}
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
                    )
        except Exception as e:
            self._log.error(
                "call of adapter or xml conversion of configs failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="internal server error",
            )

    async def import_scan_config(
        self, *, file: Annotated[bytes, File()]
    ) -> ImportConfigResponse:
        try:
            resp = self.gvm_configs.import_scan_config(file)
            return {"id": resp.get("id")}
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
                    )
        except Exception as e:
            self._log.error(
                "call of adapter or xml conversion of configs failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="internal server error",
            )
