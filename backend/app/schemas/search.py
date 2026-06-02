from app.schemas.article import ArticleListItemResponse
from app.schemas.quick_post import QuickPostResponse
from pydantic import BaseModel


class SearchResponse(BaseModel):
    query: str
    articles: list[ArticleListItemResponse]
    quick_posts: list[QuickPostResponse]
