from datetime import UTC, datetime

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, element


class SyncNotAvailableError(BaseXmlModel, search_mode="unordered", tag="error"):
    pass


class SyncNotAvailable(BaseXmlModel, search_mode="unordered", tag="sync_not_available"):
    error: SyncNotAvailableError | None = element(default=None)


class CurrentlySyncing(BaseXmlModel, search_mode="unordered", tag="currently_syncing"):
    timestamp: str | None = element(default=None)


class Feed(BaseXmlModel, search_mode="unordered", tag="feed"):
    type: str | None = element(default=None)
    name: str | None = element(default=None)
    version: str | None = element(default=None)
    description: str | None = element(default=None)
    sync_not_available: SyncNotAvailable | None = element(default=None)
    currently_syncing: CurrentlySyncing | None = element(default=None)

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
                return datetime.strptime(self.version.strip(), fmt).replace(tzinfo=UTC).timestamp()
            except ValueError:
                continue
        return 0


class Feeds(BaseXmlModel, search_mode="unordered", tag="get_feeds_response"):
    feed_owner_set: bool | None = element(default=None)
    feed_roles_set: bool | None = element(default=None)
    feed_resources_access: bool | None = element(default=None)
    feeds: list[Feed] = element(tag="feed", default_factory=list)


class GetFeedsResponse(BaseModel):
    feeds: list[Feed]
