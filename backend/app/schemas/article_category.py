from pydantic import BaseModel, Field


class ArticleCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=40)


class ArticleCategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str
    sort_order: int
    create_time: str


class ArticleCategoryListResponse(BaseModel):
    items: list[ArticleCategoryResponse]
