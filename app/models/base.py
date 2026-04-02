from datetime import datetime
from typing import Optional

from pydantic_xml import BaseXmlModel, element, attr, wrapped


class Permission(BaseXmlModel, tag="permission"):
    name: str = element()


class Owner(BaseXmlModel, tag="owner"):
    name: str = element(default="")


class UserTag(BaseXmlModel, tag="tag"):
    id: str = attr()
    name: str = element()
    value: str = element()
    comment: str = element(default="")


class UserTags(BaseXmlModel, tag="user_tags"):
    count: int = element(default=0)
    tags: Optional[list[UserTag]] = element(tag="tag", default=None)


class BaseXmlGvmModel(BaseXmlModel):
    id: str = attr()
    owner: Owner = element()
    name: str = element()
    comment: str = element(default="")
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    permissions: list[Permission] = wrapped("permissions", element(tag="permission"))
    user_tags: Optional[UserTags] = element("user_tags", default=None)


class CertificateInfo(BaseXmlModel):
    time_status: str = element()
    activation_time: datetime = element()
    expiration_time: datetime = element()
    issuer: str = element()
    md5_fingerprint: str = element()


class ResultCount(BaseXmlModel, tag="result_count"):
    false_positive: int = element(default=0)
    log: int = element(default=0)
    info: int = element(default=0)
    warning: int = element(default=0)
    hole: int = element(default=0)
