from xml.etree.ElementTree import ElementTree


def status_response_code_ok(root: ElementTree, status_code: int) -> bool:
    return int(root.get("status")) == status_code
