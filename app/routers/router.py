# pylint: disable=raise-missing-from
from typing import Dict

from fastapi import FastAPI
from structlog.stdlib import BoundLogger

from app.config import VERSION, COMMIT, BUILD_AT
from app.gvm_tools.configs import GVMConfigs
from app.gvm_tools.port_lists import GVMPortLists
from app.gvm_tools.reports import GVMReports
from app.gvm_tools.scanners import GVMScanners
from app.gvm_tools.schedules import GVMSchedules
from app.gvm_tools.targets import GVMTargets
from app.gvm_tools.tasks import GVMTasks
from app.routers.configs import ConfigsRouter
from app.routers.port_lists import PortListsRouter
from app.routers.reports import ReportsRouter
from app.routers.scanners import ScannersRouter
from app.routers.schedules import SchedulesRouter
from app.routers.targets import TargetsRouter
from app.routers.tasks import TasksRouter


class App:
    # pylint: disable=too-many-positional-arguments
    def __init__(
            self,
            gvm_targets: GVMTargets,
            gvm_port_lists: GVMPortLists,
            gvm_tasks: GVMTasks,
            gvm_configs: GVMConfigs,
            gvm_scanners: GVMScanners,
            gvm_schedules: GVMSchedules,
            gvm_reports: GVMReports,
            log: BoundLogger
    ) -> None:
        self.fastapi = FastAPI()
        self.fastapi.add_api_route("/health", self.health, methods=["GET"])
        self.fastapi.include_router(TargetsRouter(gvm_targets, log))
        self.fastapi.include_router(PortListsRouter(gvm_port_lists, log))
        self.fastapi.include_router(TasksRouter(gvm_tasks, log))
        self.fastapi.include_router(ConfigsRouter(gvm_configs, log))
        self.fastapi.include_router(ScannersRouter(gvm_scanners, log))
        self.fastapi.include_router(SchedulesRouter(gvm_schedules, log))
        self.fastapi.include_router(ReportsRouter(gvm_reports, log))
        self._log = log

    @staticmethod
    def health() -> Dict[str, str]:
        return {"status": "ok", "version": VERSION, "commit": COMMIT, "build_at": BUILD_AT}
