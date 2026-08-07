# pylint: disable=raise-missing-from
import traceback
from typing import Dict, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from app.gvm_tools.tasks import GVMTasks
from app.models.tasks import Task, TaskCreate, TaskUpdate, GetTaskResponse, GetTasksResponse, \
    CreateTaskResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR, BAD_REQUEST, NOT_FOUND


class TasksRouter(APIRouter):
    def __init__(self, gvm_tasks: GVMTasks, log: BoundLogger) -> None:
        super().__init__(
            prefix="/v1/tasks",
            tags=["tasks"],
            dependencies=[Depends(authorization)]
        )
        self._gvm_tasks = gvm_tasks
        self._log = log

        # GET Task
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.get_task,
            methods=["GET"],
            response_model=GetTaskResponse,
            responses=http_responses
        )

        # GET Tasks
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_tasks,
            methods=["GET"],
            response_model=GetTasksResponse,
            responses=http_responses
        )

        # POST Create Tasks
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(BAD_REQUEST)
        self.add_api_route(
            "",
            self.create_task,
            methods=["POST"],
            status_code=201,
            response_model=CreateTaskResponse,
            response_description="uuid of the created task",
            responses=http_responses
        )

        # PUT Task
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.update_task,
            methods=["PUT"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

        # DELETE Task
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}",
            self.delete_task,
            methods=["DELETE"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

        # POST Start Task
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}/start",
            self.start_task,
            methods=["POST"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

        # POST Stop Task
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}/stop",
            self.stop_task,
            methods=["POST"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

        # POST Resume Task
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(NOT_FOUND)
        self.add_api_route(
            "/{uuid}/resume",
            self.resume_task,
            methods=["POST"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

    async def get_task(self, uuid: str) -> Dict[str, Task]:
        try:
            resp = self._gvm_tasks.get_task(uuid)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="target not found"
                    )
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status,
                                    traceback=traceback.format_exc())
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )
        task = resp.findall("./task")
        if len(task) > 1:
            self._log.error("multiple tasks with same uuid found")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="multiple tasks with same uuid found"
            )
        return {"task": Task.from_xml(tostring(task[0]))}

    async def get_tasks(self, filter_str: Optional[str] = None, trash: Optional[bool] = False,
                        details: Optional[bool] = False) -> Dict[
        str, list[Task]]:
        try:
            resp = self._gvm_tasks.get_tasks(filter_str, trash, details)
        except GvmResponseError as e:
            match e.status:
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status,
                                    traceback=traceback.format_exc())
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )
        tasks = resp.findall("./task")
        res = []
        for t in tasks:
            res.append(Task.from_xml(tostring(t)))
        return {"tasks": res}

    async def create_task(self, task: TaskCreate) -> Dict[str, str]:
        try:
            resp = self._gvm_tasks.create_task(**task.__dict__)
        except GvmResponseError as e:
            match e.status:
                case "400":
                    if "Task exists already" in e.message:
                        filter_str: Optional[str] = 'name="' + task.name + '"'
                        resp = self._gvm_tasks.get_tasks(filter_str=filter_str, trash=False, details=False)
                        tasks = resp.findall("./task")
                        if len(tasks) > 1:
                            raise HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="status code not ok"
                            )
                        return {"id": Task.from_xml(tostring(tasks[0])).id}
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status,
                                    traceback=traceback.format_exc())
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )
        return {"id": resp.get("id")}

    async def update_task(self, uuid: str, task: TaskUpdate) -> None:
        try:
            _ = self._gvm_tasks.update_task(uuid, **task.__dict__)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="target not found"
                    )
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status,
                                    traceback=traceback.format_exc())
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )

    async def delete_task(self, uuid: str, ultimate: Optional[bool] = False) -> None:
        try:
            _ = self._gvm_tasks.delete_task(uuid, ultimate=ultimate)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="target not found"
                    )
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status,
                                    traceback=traceback.format_exc())
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )

    async def start_task(self, uuid: str) -> None:
        try:
            _ = self._gvm_tasks.start_task(uuid)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="target not found"
                    )
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status,
                                    traceback=traceback.format_exc())
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )

    async def resume_task(self, uuid: str) -> None:
        try:
            _ = self._gvm_tasks.resume_task(uuid)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="target not found"
                    )
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status,
                                    traceback=traceback.format_exc())
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )

    async def stop_task(self, uuid: str) -> None:
        try:
            _ = self._gvm_tasks.stop_task(uuid)
        except GvmResponseError as e:
            match e.status:
                case "404":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="target not found"
                    )
                case _:
                    self._log.error("call of adapter failed", error=e, status_code=e.status,
                                    traceback=traceback.format_exc())
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="status code not ok"
                    )
