from typing import Optional

from pydantic import BaseModel
from pydantic_xml import element, BaseXmlModel


class SyncNotAvailableError(BaseXmlModel, search_mode="unordered", tag="error"):
    pass


class SyncNotAvailable(BaseXmlModel, search_mode="unordered", tag="sync_not_available"):
    error: Optional[SyncNotAvailableError] = element(default=None)


class CurrentlySyncing(BaseXmlModel, search_mode="unordered", tag="currently_syncing"):
    timestamp: Optional[str] = element(default=None)


class Feed(BaseXmlModel, search_mode="unordered", tag="feed"):
    type: Optional[str] = element(default=None)
    name: Optional[str] = element(default=None)
    version: Optional[str] = element(default=None)
    description: Optional[str] = element(default=None)
    sync_not_available: Optional[SyncNotAvailable] = element(default=None)
    currently_syncing: Optional[CurrentlySyncing] = element(default=None)


class Feeds(BaseXmlModel, search_mode="unordered", tag="get_feeds_response"):
    feed_owner_set: Optional[bool] = element(default=None)
    feed_roles_set: Optional[bool] = element(default=None)
    feed_resources_access: Optional[bool] = element(default=None)
    feeds: list[Feed] = element(tag="feed", default_factory=list)


class GetFeedsResponse(BaseModel):
    feeds: list[Feed]
