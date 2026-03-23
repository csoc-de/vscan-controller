from typing import Dict, Any
from fastapi import FastAPI

from app.gvm_tools.targets import GVMTargets
from app.routers.targets import TargetsRouter

class App:
    def __init__(self, gvm_targets: GVMTargets) -> None:
        self.fastapi = FastAPI()
        self.fastapi.add_api_route("/health", self.health, methods=["GET"])
        self.fastapi.include_router(TargetsRouter(gvm_targets))

    @staticmethod
    def health() -> Dict[str, str]:
        return {"status": "ok"}