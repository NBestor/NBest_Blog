from pydantic import BaseModel, Field


class AdminUserResponse(BaseModel):
    id: int
    username: str
    nickname: str
    avatar_url: str | None
    signature: str | None
    role: str
    create_time: str
    has_avatar: bool
    is_supervisor: bool
    can_manage: bool
    can_change_role: bool


class AdminUserListResponse(BaseModel):
    items: list[AdminUserResponse]


class AdminRenameRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")


class AdminRoleRequest(BaseModel):
    role: str = Field(pattern="^(user|admin)$")


class AdminArticleResponse(BaseModel):
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
    author_nickname: str


class AdminArticleListResponse(BaseModel):
    items: list[AdminArticleResponse]


class AdminQuickPostResponse(BaseModel):
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


class AdminQuickPostListResponse(BaseModel):
    items: list[AdminQuickPostResponse]


class AdminCommentResponse(BaseModel):
    id: int
    user_id: int
    article_id: int | None
    author_nickname: str
    content: str
    create_time: str
    target_type: str
    target_id: int


class AdminCommentListResponse(BaseModel):
    items: list[AdminCommentResponse]


class AdminSummaryResponse(BaseModel):
    users: int
    admins: int
    articles: int
    quick_posts: int
    comments: int
    photos: int
