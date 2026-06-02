from pydantic import BaseModel


class ArticleTagResponse(BaseModel):
    id: int
    user_id: int
    name: str
    create_time: str


class ArticleTagListResponse(BaseModel):
    items: list[ArticleTagResponse]
