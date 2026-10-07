import threading
from datetime import datetime, timezone
from xml.etree.ElementTree import tostring

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform
from prometheus_client import Gauge
from structlog.stdlib import BoundLogger

from app.models.feeds import Feeds

FEED_VERSION_FORMATS = (
    "%Y%m%d%H%M",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d",
)


class Metrics:
    # pylint: disable=too-many-positional-arguments,too-many-instance-attributes
    def __init__(
            self,
            socket: UnixSocketConnection,
            transform: EtreeCheckCommandTransform,
            user: str,
            password: str,
            interval_seconds: int,
            log: BoundLogger
    ) -> None:
        self._socket = socket
        self._transform = transform
        self._user = user
        self._password = password
        self._interval_seconds = interval_seconds
        self._log = log
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._gvm_feed_version = Gauge(
            "gvm_feed_version",
            "Version of the GVM feed as epoch seconds; 0 if the version could not be parsed",
            ["feed_name", "feed_type"]
        )

    def start(self) -> None:
        self._stop_event.clear()
        thread: threading.Thread = threading.Thread(target=self._run, name="gvm-feed-metrics", daemon=True)
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
            with GMP(connection=self._socket, transform=self._transform) as gmp:
                gmp.authenticate(self._user, self._password)
                resp = gmp.get_feeds()
            feeds: Feeds = Feeds.from_xml(tostring(resp))
            for feed in feeds.feeds:
                labels = {"feed_name": feed.name or "", "feed_type": feed.type or ""}
                self._gvm_feed_version.labels(**labels).set(self._parse_version(feed.version))
        except Exception as e:  # pylint: disable=broad-exception-caught
            self._log.warning("updating feed version metrics failed, keeping last values", error=e)

    @staticmethod
    def _parse_version(version: str | None) -> float:
        if version is None:
            return 0
        for fmt in FEED_VERSION_FORMATS:
            try:
                return datetime.strptime(version.strip(), fmt).replace(tzinfo=timezone.utc).timestamp()
            except ValueError:
                continue
        return 0
