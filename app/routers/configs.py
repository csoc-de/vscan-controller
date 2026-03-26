from typing import Dict, List, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from structlog.stdlib import BoundLogger

from app.gvm_tools.configs import GVMConfigs
from app.gvm_tools.gvm import status_response_code_ok, get_status_response_code
from app.models.configs import Config, GetConfigsResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR


class ConfigsRouter(APIRouter):
    def __init__(self, gvm_configs: GVMConfigs, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/configs",
            tags=["configs"],
            dependencies=[Depends(authorization)]
        )
        self.gvm_configs = gvm_configs
        self._log = log

        # GET Port Lists
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_configs,
            methods=["GET"],
            response_model=GetConfigsResponse,
            responses=http_responses
        )

    async def get_configs(
            self,
            *,
            filter_string: Optional[str] = None,
            trash: Optional[bool] = None,
            details: Optional[bool] = None,
            families: Optional[bool] = None,
            preferences: Optional[bool] = None,
            tasks: Optional[bool] = None,
    ) -> Dict[str, List[Config]]:
        resp = self.gvm_configs.get_configs(filter_string=filter_string, trash=trash, details=details,
                                            families=families, preferences=preferences, tasks=tasks)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
        configs = resp.findall("./config")
        res = []
        for r in configs:
            res.append(Config.from_xml(tostring(r)))
        return {"configs": res}
