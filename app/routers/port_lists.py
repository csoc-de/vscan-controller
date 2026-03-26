from typing import Dict, List, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from structlog.stdlib import BoundLogger

from app.gvm_tools.gvm import status_response_code_ok, get_status_response_code
from app.gvm_tools.port_lists import GVMPortLists
from app.models.port_lists import PortList, GetPortListsResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR


class PortListsRouter(APIRouter):
    def __init__(self, gvm_port_lists: GVMPortLists, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/port-lists",
            tags=["port_lists"],
            dependencies=[Depends(authorization)]
        )
        self._gvm_port_lists = gvm_port_lists
        self._log = log

        # GET Port Lists
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_port_lists,
            methods=["GET"],
            response_model=GetPortListsResponse,
            responses=http_responses
        )

    async def get_port_lists(
            self,
            *,
            filter_str: Optional[str] = None,
            details: Optional[bool] = False,
            trash: Optional[bool] = False
    ) -> Dict[str, List[PortList]]:
        resp = self._gvm_port_lists.get_port_lists(filter_str=filter_str, details=details, trash=trash)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
        port_lists = resp.findall("./port_list")
        res = []
        for l in port_lists:
            res.append(PortList.from_xml(tostring(l)))
        return {"port_lists": res}
