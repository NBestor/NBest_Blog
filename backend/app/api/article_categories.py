from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth import getCurrentUser
from app.schemas.article_category import ArticleCategoryListResponse, ArticleCategoryRequest, ArticleCategoryResponse
from app.services.article_category_service import createCategory, listCategories


router = APIRouter(prefix="/article-categories", tags=["article-categories"])


@router.get("", response_model=ArticleCategoryListResponse)
def getArticleCategories(
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> ArticleCategoryListResponse:
    return ArticleCategoryListResponse(items=listCategories(int(currentUser["id"])))


@router.post("", response_model=ArticleCategoryResponse, status_code=status.HTTP_201_CREATED)
def createArticleCategory(
    request: ArticleCategoryRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> ArticleCategoryResponse:
    category = createCategory(int(currentUser["id"]), request.name)
    if category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")

    return ArticleCategoryResponse(**category)
