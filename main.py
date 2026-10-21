import sys
import traceback
from typing import Any

import structlog
import uvicorn
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform

from app.config import (
    FEEDS_METRICS_INTERVAL_SECONDS,
    GREENBONE_PASSWORD,
    GREENBONE_SOCKET_PATH,
    GREENBONE_USER,
    HOST,
    LOG_LEVEL,
    PORT,
)
from app.gvm_tools.configs import GVMConfigs
from app.gvm_tools.feeds import GVMFeeds
from app.gvm_tools.port_lists import GVMPortLists
from app.gvm_tools.reports import GVMReports
from app.gvm_tools.scanners import GVMScanners
from app.gvm_tools.schedules import GVMSchedules
from app.gvm_tools.targets import GVMTargets
from app.gvm_tools.tasks import GVMTasks
from app.metrics import Metrics
from app.routers.router import App
from app.utils.processors import add_and_modify_parameters, add_log_level_upper


def init_logging() -> Any | None:
    try:
        structlog.configure(
            processors=[
                add_log_level_upper,
                structlog.processors.CallsiteParameterAdder(
                    [
                        structlog.processors.CallsiteParameter.PATHNAME,
                        structlog.processors.CallsiteParameter.FUNC_NAME,
                        structlog.processors.CallsiteParameter.LINENO,
                        structlog.processors.CallsiteParameter.MODULE,
                    ],
                ),
                add_and_modify_parameters,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.dict_tracebacks,
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="time"),
                structlog.processors.EventRenamer("msg"),
                structlog.contextvars.merge_contextvars,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
        return structlog.get_logger()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"could not setup logger error: {e}")
        print(traceback.format_exc())
        raise e


def main() -> int:
    try:
        logger = init_logging()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"could not setup logger\n ERROR: {e}\n{traceback.format_exc()}")
        return 1
    try:
        socket: UnixSocketConnection = UnixSocketConnection(path=GREENBONE_SOCKET_PATH)
        metrics_socket: UnixSocketConnection = UnixSocketConnection(path=GREENBONE_SOCKET_PATH)
        transform: EtreeCheckCommandTransform = EtreeCheckCommandTransform()
        with GMP(connection=socket) as gmp:
            print(gmp.get_version())
        app = App(
            GVMTargets(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
            GVMPortLists(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
            GVMTasks(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
            GVMConfigs(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
            GVMScanners(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
            GVMSchedules(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
            GVMReports(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
            GVMFeeds(socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
            Metrics(
                GVMFeeds(metrics_socket, transform, GREENBONE_USER, GREENBONE_PASSWORD),
                FEEDS_METRICS_INTERVAL_SECONDS,
                log=logger
            ),
            log=logger,
        )
        uvicorn.run(app.fastapi, host=HOST, port=PORT, log_level="info")
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e, traceback=traceback.format_exc())
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
