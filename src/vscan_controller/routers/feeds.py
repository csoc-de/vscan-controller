# pylint: disable=raise-missing-from
import traceback
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status
from gvm.errors import GvmResponseError
from structlog.stdlib import BoundLogger

from vscan_controller.gvm_tools.feeds import GVMFeeds
from vscan_controller.models.feeds import Feed, Feeds, GetFeedsResponse
from vscan_controller.routers.auth import authorization
from vscan_controller.routers.response import INTERNAL_SERVER_ERROR, UNAUTHORIZED


class FeedsRouter(APIRouter):
    def __init__(self, gvm_feeds: GVMFeeds, log: BoundLogger) -> None:
        super().__init__(prefix="/v1/feeds", tags=["feeds"], dependencies=[Depends(authorization)])
        self._gvm_feeds = gvm_feeds
        self._log = log

        # GET Feeds
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_feeds,
            methods=["GET"],
            response_model=GetFeedsResponse,
            responses=http_responses,
        )

    async def get_feeds(
        self,
    ) -> dict[str, list[Feed]]:
        try:
            resp = self._gvm_feeds.get_feeds()
            print(tostring(resp))
            res = Feeds.from_xml(tostring(resp))
            return {"feeds": res.feeds}
        except GvmResponseError as e:
            match e.status:
                case _:
                    self._log.error(
                        "call of adapter failed",
                        error=e,
                        status_code=e.status,
                        traceback=traceback.format_exc(),
                    )
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="internal server error",
                    ) from e
        except Exception as e:
            self._log.error(
                "call of adapter or xml conversion of feeds failed",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
            ) from e
