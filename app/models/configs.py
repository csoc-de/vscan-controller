from typing import List

from pydantic import BaseModel
from pydantic_xml import element

from app.models.base import BaseXmlGvmModel


class Config(BaseXmlGvmModel, tag="config"):
    family_count: int = element()
    nvt_count: int = element()
    type: int = element()
    usage_type: str = element()
    predefined: int = element()


class GetConfigsResponse(BaseModel):
    configs: List[Config]
