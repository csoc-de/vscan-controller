# pylint: disable=raise-missing-from
import traceback
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from vscan_controller.gvm_tools.targets import GVMTargets
from vscan_controller.models.targets import (
    CreateTargetResponse,
    GetTargetResponse,
    GetTargetsResponse,
    Target,
    TargetCreate,
    TargetUpdate,
)
from vscan_controller.routers.auth import authorization
from vscan_controller.routers.response import (
    BAD_REQUEST,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND,
    UNAUTHORIZED,
)


class TargetsRouter(APIRouter):
    def __init__(self, gvm_targets: GVMTargets, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/targets", tags=["targets"], dependencies=[Depends(authorization)]
        )
        self._gvm_targets = gvm_targets
        self._log = log

        # GET Target
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.get_target,
            methods=["GET"],
            response_model=GetTargetResponse,
            responses=http_responses,
        )

        # GET Targets
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_targets,
            methods=["GET"],
            response_model=GetTargetsResponse,
            responses=http_responses,
        )

        # POST Create Targets
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(BAD_REQUEST)
        self.add_api_route(
            "",
            self.create_target,
            methods=["POST"],
            status_code=201,
            response_model=CreateTargetResponse,
            response_description="uuid of the created target",
            responses=http_responses,
        )

        # PUT Target
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.update_target,
            methods=["PUT"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

        # DELETE Target
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.delete_target,
            methods=["DELETE"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

    async def get_target(self, uuid: str) -> dict[str, Target]:
        try:
            resp = self._gvm_targets.get_target(uuid)
            target = resp.findall("./target")
            if len(target) > 1:
                self._log.error("multiple targets with same uuid found")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="multiple targets with same uuid found",
                )
            return {"target": Target.from_xml(tostring(target[0]))}
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
                "call of adapter or xml conversion of target failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def get_targets(
        self, filter_string: str | None = None, trash: bool | None = False
    ) -> dict[str, list[Target]]:
        try:
            resp = self._gvm_targets.get_targets(filter_string, trash)
            targets = resp.findall("./target")
            res = []
            for t in targets:
                res.append(Target.from_xml(tostring(t)))
            return {"targets": res}
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
                "call of adapter or xml conversion of targets failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def create_target(self, target: TargetCreate) -> dict[str, str]:
        if target.port_range is None and target.port_list_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="one of port_list_id or port_range are required",
            )
        try:
            resp = self._gvm_targets.create_target(**target.__dict__)
            return {"id": resp.get("id")}
        except GvmResponseError as e:
            match e.status:
                case "400":
                    self._log.error(
                        "target already exists or new target has an invalid value",
                        error=e,
                        status_code=e.status,
                        traceback=traceback.format_exc(),
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="target already exists or new target has an invalid value",
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
                "call of adapter or get of target id failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def update_target(self, uuid: str, target: TargetUpdate) -> None:
        try:
            _ = self._gvm_targets.update_target(uuid, **target.__dict__)
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
                "call of adapter or update of target failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e

    async def delete_target(self, uuid: str, ultimate: bool | None = False) -> None:
        try:
            _ = self._gvm_targets.delete_target(uuid, ultimate=ultimate)
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
                "call of adapter or delete of target failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e
