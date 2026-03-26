from typing import Dict, List, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from structlog.stdlib import BoundLogger

from app.gvm_tools.gvm import status_response_code_ok, get_status_response_code
from app.gvm_tools.tasks import GVMTasks
from app.models.tasks import Task, TaskCreate, TaskUpdate, GetTaskResponse, GetTasksResponse, \
    CreateTaskResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR, BAD_REQUEST


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
        self.add_api_route(
            "/{uuid}",
            self.delete_task,
            methods=["DELETE"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

    async def get_task(self, uuid: str) -> Dict[str, Task]:
        resp = self._gvm_tasks.get_task(uuid)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
        task = resp.findall("./task")
        if len(task) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="task not found"
            )
        if len(task) > 1:
            self._log.error("multiple tasks with same uuid found")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="multiple tasks with same uuid found"
            )
        return {"task": Task.from_xml(tostring(task[0]))}

    async def get_tasks(self, filter_str: Optional[str] = None, trash: Optional[bool] = False,
                        details: Optional[bool] = False) -> Dict[
        str, List[Task]]:
        resp = self._gvm_tasks.get_tasks(filter_str, trash, details)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
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
        resp = self._gvm_tasks.create_task(**task.__dict__)
        if not status_response_code_ok(resp, 201):
            self._log.error("status code not created", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not created"
            )
        return {"id": resp.get("id")}

    async def update_task(self, uuid: str, task: TaskUpdate) -> None:
        resp = self._gvm_tasks.update_task(uuid, **task.__dict__)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )

    async def delete_task(self, uuid: str, ultimate: Optional[bool] = False) -> None:
        resp = self._gvm_tasks.delete_task(uuid, ultimate=ultimate)
        if not status_response_code_ok(resp, 200):
            self._log.error("status code not ok", status_code=get_status_response_code(resp))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
