from pydantic import BaseModel
from typing import List
from enum import Enum

class ShareObjectType(str, Enum):
    GROUP = "group"
    WEBPAGE = "webpage"


class ShareObject(BaseModel):
    type: ShareObjectType
    title: str
    data: str

class SharePayload(BaseModel):
    type: ShareObjectType
    title: str
    data: List[ShareObject]

class ShareResponse(BaseModel):
    share_id: str 