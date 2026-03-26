from datetime import datetime
from typing import List

from pydantic_xml import BaseXmlModel, element, attr, wrapped


class Permission(BaseXmlModel, tag="permission"):
    name: str = element()


class Owner(BaseXmlModel, tag="owner"):
    name: str = element(default="")


class BaseXmlGvmModel(BaseXmlModel):
    id: str = attr()
    owner: Owner = element()
    name: str = element()
    comment: str = element(default="")
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    permissions: List[Permission] = wrapped("permissions", element())
