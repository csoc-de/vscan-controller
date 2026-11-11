from datetime import datetime

from pydantic_xml import BaseXmlModel, attr, element, wrapped


class Permission(BaseXmlModel, search_mode="unordered", tag="permission"):
    name: str = element()


class Owner(BaseXmlModel, search_mode="unordered", tag="owner"):
    name: str | None = element(default=None)


class UserTag(BaseXmlModel, search_mode="unordered", tag="tag"):
    id: str = attr()
    name: str = element()
    value: str = element()
    comment: str | None = element(default=None)


class UserTags(BaseXmlModel, search_mode="unordered", tag="user_tags"):
    count: int | None = element(default=None)
    tags: list[UserTag] | None = element(tag="tag", default=None)


class BaseXmlGvmModel(BaseXmlModel, search_mode="unordered"):
    id: str = attr()
    owner: Owner = element()
    name: str = element()
    comment: str | None = element(default=None)
    creation_time: datetime = element()
    modification_time: datetime = element()
    writable: bool = element()
    in_use: bool = element()
    permissions: list[Permission] = wrapped("permissions", element(tag="permission"))
    user_tags: UserTags | None = element("user_tags", default=None)
