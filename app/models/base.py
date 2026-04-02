from datetime import datetime
from typing import Optional

from pydantic_xml import BaseXmlModel, element, attr, wrapped


class Permission(BaseXmlModel, search_mode="unordered", tag="permission"):
    name: str = element()


class Owner(BaseXmlModel, search_mode="unordered", tag="owner"):
    name: Optional[str] = element(default=None)


class UserTag(BaseXmlModel, search_mode="unordered", tag="tag"):
    id: str = attr()
    name: str = element()
    value: str = element()
    comment: Optional[str] = element(default=None)


class UserTags(BaseXmlModel, search_mode="unordered", tag="user_tags"):
    count: Optional[int] = element(default=None)
    tags: Optional[list[UserTag]] = element(tag="tag", default=None)


class BaseXmlGvmModel(BaseXmlModel, search_mode="unordered"):
    id: str = attr()
    owner: Owner = element()
    name: str = element()
    comment: Optional[str] = element(default=None)
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    permissions: list[Permission] = wrapped("permissions", element(tag="permission"))
    user_tags: Optional[UserTags] = element("user_tags", default=None)


class CertificateInfo(BaseXmlModel, search_mode="unordered"):
    time_status: str = element()
    activation_time: datetime = element()
    expiration_time: datetime = element()
    issuer: str = element()
    md5_fingerprint: str = element()
