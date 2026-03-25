from typing import Dict

from fastapi import FastAPI
from structlog.stdlib import BoundLogger

from app.config import VERSION, COMMIT, BUILD_AT
from app.gvm_tools.port_lists import GVMPortLists
from app.gvm_tools.targets import GVMTargets
from app.routers.port_lists import PortListsRouter
from app.routers.targets import TargetsRouter


class App:
    def __init__(self, gvm_targets: GVMTargets, gvm_port_lists: GVMPortLists, log: BoundLogger) -> None:
        self.fastapi = FastAPI()
        self.fastapi.add_api_route("/health", self.health, methods=["GET"])
        self.fastapi.include_router(TargetsRouter(gvm_targets, log))
        self.fastapi.include_router(PortListsRouter(gvm_port_lists, log))
        self._log = log

        self._log.debug("Test Debug", test="test1")
        self._log.info("Test Info", test="test2")
        self._log.warning("Test Warning", test="test3")
        self._log.error("Test Error", test="test4")

    @staticmethod
    def health() -> Dict[str, str]:
        return {"status": "ok", "version": VERSION, "commit": COMMIT, "build_at": BUILD_AT}
