from pydantic import BaseModel, Field


class CommentRequest(BaseModel):
    content: str = Field(min_length=1, max_length=500)
    parent_id: int | None = None


class CommentResponse(BaseModel):
    id: int
    user_id: int
    article_id: int | None
    parent_id: int | None
    author_nickname: str
    content: str
    create_time: str
    like_count: int = 0
    is_liked: bool = False
    children: list["CommentResponse"] = Field(default_factory=list)


class CommentListResponse(BaseModel):
    items: list[CommentResponse]
