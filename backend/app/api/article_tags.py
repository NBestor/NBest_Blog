from fastapi import APIRouter, Depends

from app.api.auth import getCurrentUser
from app.schemas.article_tag import ArticleTagListResponse
from app.services.article_tag_service import listTags


router = APIRouter(prefix="/article-tags", tags=["article-tags"])


@router.get("", response_model=ArticleTagListResponse)
def getArticleTags(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> ArticleTagListResponse:
    return ArticleTagListResponse(items=listTags(int(currentUser["id"])))
