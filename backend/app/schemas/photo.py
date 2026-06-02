from pydantic import BaseModel, Field


class PhotoResponse(BaseModel):
    id: int
    user_id: int
    author_nickname: str
    url: str
    source_type: str
    visible_type: str
    upload_time: str
    can_manage: bool = False


class PhotoListResponse(BaseModel):
    items: list[PhotoResponse]


class PhotoUpdateRequest(BaseModel):
    visible_type: str = Field(pattern="^(public|self)$")
