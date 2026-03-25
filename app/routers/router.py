from typing import Dict

from fastapi import FastAPI

from app.config import VERSION, COMMIT, BUILD_AT
from app.gvm_tools.port_lists import GVMPortLists
from app.gvm_tools.targets import GVMTargets
from app.routers.port_lists import PortListsRouter
from app.routers.targets import TargetsRouter


class App:
    def __init__(self, gvm_targets: GVMTargets, gvm_port_lists: GVMPortLists) -> None:
        self.fastapi = FastAPI()
        self.fastapi.add_api_route("/health", self.health, methods=["GET"])
        self.fastapi.include_router(TargetsRouter(gvm_targets))
        self.fastapi.include_router(PortListsRouter(gvm_port_lists))

    @staticmethod
    def health() -> Dict[str, str]:
        return {"status": "ok", "version": VERSION, "commit": COMMIT, "build_at": BUILD_AT}
