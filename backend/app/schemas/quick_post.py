from pydantic import BaseModel, Field


class QuickPostRequest(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
    visible_type: str | None = Field(default=None, pattern="^(public|friend|self)$")


class QuickPostResponse(BaseModel):
    id: int
    user_id: int
    author_nickname: str
    content: str
    visible_type: str
    create_time: str
    update_time: str
    like_count: int
    comment_count: int
    is_liked: bool = False
    can_manage: bool = False


class QuickPostListResponse(BaseModel):
    items: list[QuickPostResponse]
