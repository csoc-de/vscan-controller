from typing import Dict, List, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from structlog.stdlib import BoundLogger

from app.gvm_tools.gvm import status_response_code_ok, get_status_response_code
from app.gvm_tools.schedules import GVMSchedules
from app.models.schedules import Schedule, ScheduleCreate, ScheduleUpdate, GetScheduleResponse, GetSchedulesResponse, \
    CreateScheduleResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR, BAD_REQUEST


class SchedulesRouter(APIRouter):
    def __init__(self, gvm_schedules: GVMSchedules, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/schedules",
            tags=["schedules"],
            dependencies=[Depends(authorization)]
        )
        self._gvm_schedules = gvm_schedules
        self._log = log

        # GET Schedule
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "/{uuid}",
            self.get_schedule,
            methods=["GET"],
            response_model=GetScheduleResponse,
            responses=http_responses
        )

        # GET Schedules
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_schedules,
            methods=["GET"],
            response_model=GetSchedulesResponse,
            responses=http_responses
        )

        # POST Create Schedules
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(BAD_REQUEST)
        self.add_api_route(
            "",
            self.create_schedule,
            methods=["POST"],
            status_code=201,
            response_model=CreateScheduleResponse,
            response_description="uuid of the created schedule",
            responses=http_responses
        )

        # PUT Schedule
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "/{uuid}",
            self.update_schedule,
            methods=["PUT"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

        # DELETE Schedule
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "/{uuid}",
            self.delete_schedule,
            methods=["DELETE"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

    async def get_schedule(self, uuid: str, tasks: Optional[bool] = False) -> Dict[str, Schedule]:
        resp = self._gvm_schedules.get_schedule(uuid, tasks=tasks)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
        schedule = resp.findall("./schedule")
        if len(schedule) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="schedule not found"
            )
        if len(schedule) > 1:
            self._log.error("multiple schedules with same uuid found")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="multiple schedules with same uuid found"
            )
        return {"schedule": Schedule.from_xml(tostring(schedule[0]))}

    async def get_schedules(
            self,
            filter_str: Optional[str] = None,
            trash: Optional[bool] = False,
            tasks: Optional[bool] = False
    ) -> Dict[
        str, List[Schedule]]:
        resp = self._gvm_schedules.get_schedules(filter_string=filter_str, trash=trash, tasks=tasks)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
        schedules = resp.findall("./schedule")
        res = []
        for s in schedules:
            print(tostring(s))
            res.append(Schedule.from_xml(tostring(s)))
        return {"schedules": res}

    async def create_schedule(self, schedule: ScheduleCreate) -> Dict[str, str]:
        resp = self._gvm_schedules.create_schedule(**schedule.__dict__)
        if not status_response_code_ok(resp, 201):
            self._log.error("status code not created", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not created"
            )
        return {"id": resp.get("id")}

    async def update_schedule(self, uuid: str, schedule: ScheduleUpdate) -> None:
        resp = self._gvm_schedules.update_schedule(uuid, **schedule.__dict__)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )

    async def delete_schedule(self, uuid: str, ultimate: Optional[bool] = False) -> None:
        resp = self._gvm_schedules.delete_schedule(uuid, ultimate=ultimate)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
