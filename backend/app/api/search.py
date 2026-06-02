from fastapi import APIRouter, Depends, Query

from app.api.auth import getOptionalCurrentUser
from app.schemas.search import SearchResponse
from app.services.article_service import searchVisibleArticles
from app.services.quick_post_service import searchVisibleQuickPosts


router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
def searchContent(
    q: str = Query(default="", max_length=120),
    currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser),
) -> SearchResponse:
    query = q.strip()
    userId = int(currentUser["id"]) if currentUser else None
    return SearchResponse(
        query=query,
        articles=searchVisibleArticles(query, userId),
        quick_posts=searchVisibleQuickPosts(query, userId),
    )
