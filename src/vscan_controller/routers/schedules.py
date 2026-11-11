# pylint: disable=raise-missing-from
import traceback
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from vscan_controller.gvm_tools.schedules import GVMSchedules
from vscan_controller.models.schedules import (
    CreateScheduleResponse,
    GetScheduleResponse,
    GetSchedulesResponse,
    Schedule,
    ScheduleCreate,
    ScheduleUpdate,
)
from vscan_controller.routers.auth import authorization
from vscan_controller.routers.response import (
    BAD_REQUEST,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND,
    UNAUTHORIZED,
)


class SchedulesRouter(APIRouter):
    def __init__(self, gvm_schedules: GVMSchedules, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/schedules", tags=["schedules"], dependencies=[Depends(authorization)]
        )
        self._gvm_schedules = gvm_schedules
        self._log = log

        # GET Schedule
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.get_schedule,
            methods=["GET"],
            response_model=GetScheduleResponse,
            responses=http_responses,
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
            responses=http_responses,
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
            responses=http_responses,
        )

        # PUT Schedule
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
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
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.delete_schedule,
            methods=["DELETE"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

    async def get_schedule(self, uuid: str, tasks: bool | None = False) -> dict[str, Schedule]:
        try:
            resp = self._gvm_schedules.get_schedule(uuid, tasks=tasks)
            schedule = resp.findall("./schedule")
            if len(schedule) > 1:
                self._log.error("multiple schedules with same uuid found")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="multiple schedules with same uuid found",
                )
            return {"schedule": Schedule.from_xml(tostring(schedule[0]))}
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="schedule not found"
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
                "call of adapter or xml conversion of schedule failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def get_schedules(
        self,
        filter_string: str | None = None,
        trash: bool | None = False,
        tasks: bool | None = False,
    ) -> dict[str, list[Schedule]]:
        try:
            resp = self._gvm_schedules.get_schedules(
                filter_string=filter_string, trash=trash, tasks=tasks
            )
            schedules = resp.findall("./schedule")
            res = []
            for s in schedules:
                res.append(Schedule.from_xml(tostring(s)))
            return {"schedules": res}
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
                "call of adapter or xml conversion of schedules failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def create_schedule(self, schedule: ScheduleCreate) -> dict[str, str]:
        try:
            resp = self._gvm_schedules.create_schedule(**schedule.__dict__)
            return {"id": resp.get("id")}
        except GvmResponseError as e:
            match e.status:
                case "400":
                    self._log.error(
                        "schedule already exists or new schedule has an invalid value",
                        error=e,
                        status_code=e.status,
                        traceback=traceback.format_exc(),
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="schedule already exists or new schedule has an invalid value",
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
                "call of adapter or get of schedule id failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def update_schedule(self, uuid: str, schedule: ScheduleUpdate) -> None:
        try:
            _ = self._gvm_schedules.update_schedule(uuid, **schedule.__dict__)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="target not found"
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
                "call of adapter or update of schedule failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def delete_schedule(self, uuid: str, ultimate: bool | None = False) -> None:
        try:
            _ = self._gvm_schedules.delete_schedule(uuid, ultimate=ultimate)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="target not found"
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
                "call of adapter or delete of schedule failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e
