from datetime import datetime, timezone
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

    def version_as_unix_timestamp(self) -> float:
        _feed_version_formats = (
            "%Y%m%d%H%M",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
        )

        if self.version is None:
            return 0
        for fmt in _feed_version_formats:
            try:
                return datetime.strptime(self.version.strip(), fmt).replace(tzinfo=timezone.utc).timestamp()
            except ValueError:
                continue
        return 0


class Feeds(BaseXmlModel, search_mode="unordered", tag="get_feeds_response"):
    feed_owner_set: Optional[bool] = element(default=None)
    feed_roles_set: Optional[bool] = element(default=None)
    feed_resources_access: Optional[bool] = element(default=None)
    feeds: list[Feed] = element(tag="feed", default_factory=list)


class GetFeedsResponse(BaseModel):
    feeds: list[Feed]
