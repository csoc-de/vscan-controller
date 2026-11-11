# pylint: disable=raise-missing-from
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from structlog.stdlib import BoundLogger

from vscan_controller.config import BUILD_AT, COMMIT, VERSION
from vscan_controller.gvm_tools.configs import GVMConfigs
from vscan_controller.gvm_tools.feeds import GVMFeeds
from vscan_controller.gvm_tools.port_lists import GVMPortLists
from vscan_controller.gvm_tools.reports import GVMReports
from vscan_controller.gvm_tools.scanners import GVMScanners
from vscan_controller.gvm_tools.schedules import GVMSchedules
from vscan_controller.gvm_tools.targets import GVMTargets
from vscan_controller.gvm_tools.tasks import GVMTasks
from vscan_controller.metrics import Metrics
from vscan_controller.routers.configs import ConfigsRouter
from vscan_controller.routers.feeds import FeedsRouter
from vscan_controller.routers.port_lists import PortListsRouter
from vscan_controller.routers.reports import ReportsRouter
from vscan_controller.routers.scanners import ScannersRouter
from vscan_controller.routers.schedules import SchedulesRouter
from vscan_controller.routers.targets import TargetsRouter
from vscan_controller.routers.tasks import TasksRouter


class App:
    def __init__(
        self,
        gvm_targets: GVMTargets,
        gvm_port_lists: GVMPortLists,
        gvm_tasks: GVMTasks,
        gvm_configs: GVMConfigs,
        gvm_scanners: GVMScanners,
        gvm_schedules: GVMSchedules,
        gvm_reports: GVMReports,
        gvm_feeds: GVMFeeds,
        feed_metrics: Metrics,
        log: BoundLogger,
    ) -> None:
        self._feed_metrics = feed_metrics
        self._log = log

        @asynccontextmanager
        async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
            self._feed_metrics.start()
            yield
            self._feed_metrics.stop()

        self.fastapi = FastAPI(lifespan=lifespan)
        self.fastapi.add_api_route("/health", self.health, methods=["GET"])
        self.fastapi.add_api_route("/metrics", self.metrics, methods=["GET"])
        self.fastapi.include_router(TargetsRouter(gvm_targets, log))
        self.fastapi.include_router(PortListsRouter(gvm_port_lists, log))
        self.fastapi.include_router(TasksRouter(gvm_tasks, log))
        self.fastapi.include_router(ConfigsRouter(gvm_configs, log))
        self.fastapi.include_router(ScannersRouter(gvm_scanners, log))
        self.fastapi.include_router(SchedulesRouter(gvm_schedules, log))
        self.fastapi.include_router(ReportsRouter(gvm_reports, log))
        self.fastapi.include_router(FeedsRouter(gvm_feeds, log))

    @staticmethod
    def health() -> dict[str, str]:
        return {"status": "ok", "version": VERSION, "commit": COMMIT, "build_at": BUILD_AT}

    @staticmethod
    def metrics() -> Response:
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
