from pydantic import BaseModel, Field


VISIBLE_TYPES = {"public", "friend", "self"}


class DraftRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    summary: str | None = Field(default=None, max_length=300)
    content: str = Field(min_length=1)
    category_id: int | None = None
    visible_type: str = Field(default="self", pattern="^(public|friend|self)$")
    tags: list[str] = Field(default_factory=list, max_length=12)


class DraftResponse(BaseModel):
    id: int
    user_id: int
    title: str
    summary: str | None
    content: str
    is_draft: bool
    category_id: int | None
    category_name: str | None
    visible_type: str
    tags: list[str]
    create_time: str
    update_time: str


class DraftListResponse(BaseModel):
    items: list[DraftResponse]


class ArticleListItemResponse(DraftResponse):
    author_nickname: str
    like_count: int
    comment_count: int
    is_liked: bool = False
    is_collected: bool = False


class ArticleListResponse(BaseModel):
    items: list[ArticleListItemResponse]


class ArticleDetailResponse(ArticleListItemResponse):
    pass
