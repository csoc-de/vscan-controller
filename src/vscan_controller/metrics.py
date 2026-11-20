import threading
from xml.etree.ElementTree import tostring

from prometheus_client import Gauge
from structlog.stdlib import BoundLogger

from vscan_controller.gvm_tools.feeds import GVMFeeds
from vscan_controller.models.feeds import Feeds


class Metrics:
    def __init__(self, gvm_feeds: GVMFeeds, interval_seconds: int, log: BoundLogger) -> None:
        self._interval_seconds = interval_seconds
        self._log = log
        self._gvm_feeds = gvm_feeds
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._gvm_feed_version = Gauge(
            "gvm_feed_version",
            "Version of the GVM feed as epoch seconds; 0 if the version could not be parsed",
            ["feed_name", "feed_type"],
        )

    def start(self) -> None:
        self._stop_event.clear()
        thread: threading.Thread = threading.Thread(
            target=self._run, name="gvm-feed-metrics", daemon=True
        )
        self._thread = thread
        thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=10)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            self._update_feeds()
            self._stop_event.wait(self._interval_seconds)

    def _update_feeds(self) -> None:
        try:
            feeds: Feeds = Feeds.from_xml(tostring(self._gvm_feeds.get_feeds()))
            for feed in feeds.feeds:
                labels = {"feed_name": feed.name or "", "feed_type": feed.type or ""}
                self._gvm_feed_version.labels(**labels).set(feed.version_as_unix_timestamp())
        except Exception as e:  # noqa: BLE001 # using a blank exception to keep background thread alive
            self._log.warning("updating feed version metrics failed, keeping last values", error=e)
