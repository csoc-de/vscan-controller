from typing import Any

from structlog.types import EventDict

from app.config import VERSION


def add_log_level_upper(
        logger: Any, method_name: str, event_dict: EventDict
) -> EventDict:
    if method_name == "warning":
        method_name = "warn"

    if method_name == "exception":
        method_name = "error"

    event_dict["level"] = method_name.upper()

    return event_dict


def add_and_modify_parameters(logger: str, method_name: str, event_dict: EventDict) -> EventDict:
    if "module" in event_dict:
        event_dict["package"] = event_dict["module"]
        del event_dict["module"]
    if "exception" in event_dict:
        event_dict["source"] = event_dict["exception"]
        del event_dict["exception"]
    else:
        event_dict["source"] = {"file": event_dict["pathname"], "function": event_dict["func_name"],
                                "line": event_dict["lineno"]}
        del event_dict["pathname"], event_dict["lineno"], event_dict["func_name"]

    event_dict["version"] = VERSION
    event_dict["project_name"] = "vscan_controller"
    return event_dict
