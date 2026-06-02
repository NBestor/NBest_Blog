from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.api.auth import getCurrentUser, getOptionalCurrentUser
from app.core.config import getSettings
from app.db.database import getDatabaseConnection
from app.schemas.article import ArticleDetailResponse, ArticleListResponse, DraftListResponse, DraftRequest, DraftResponse
from app.schemas.comment import CommentListResponse, CommentRequest, CommentResponse
from app.schemas.interaction import InteractionResponse
from app.services.article_service import (
    createDraft,
    deleteDraft,
    getDraft,
    getVisibleArticle,
    listDrafts,
    listVisibleArticles,
    publishDraft,
    updateDraft,
)
from app.services.comment_service import createComment, getTargetComment, listComments
from app.services.interaction_service import collectArticle, likeArticle, likeTarget, uncollectArticle, unlikeArticle, unlikeTarget


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=ArticleListResponse)
def getArticles(
    currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser),
) -> ArticleListResponse:
    userId = int(currentUser["id"]) if currentUser else None
    return ArticleListResponse(items=listVisibleArticles(userId))


def _saveArticleImage(userId: int, uploadFile: UploadFile) -> str:
    if uploadFile.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported image type")

    settings = getSettings()
    imageDir = settings.upload_dir / "articles" / str(userId)
    imageDir.mkdir(parents=True, exist_ok=True)

    try:
        image = Image.open(BytesIO(uploadFile.file.read()))
        image.verify()
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file") from exc

    suffix = Path(uploadFile.filename or "image.png").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        suffix = ".png"

    filename = f"{uuid4().hex}{suffix}"
    imagePath = imageDir / filename
    uploadFile.file.seek(0)
    imagePath.write_bytes(uploadFile.file.read())
    return f"/static/uploads/articles/{userId}/{filename}"


@router.post("/drafts", response_model=DraftResponse, status_code=status.HTTP_201_CREATED)
def createArticleDraft(
    request: DraftRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> DraftResponse:
    draft = createDraft(
        int(currentUser["id"]),
        request.title,
        request.summary,
        request.content,
        request.category_id,
        request.visible_type,
        request.tags,
    )
    if draft is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")

    return DraftResponse(**draft)


@router.get("/drafts", response_model=DraftListResponse)
def getArticleDrafts(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> DraftListResponse:
    return DraftListResponse(items=listDrafts(int(currentUser["id"])))


@router.get("/drafts/{draft_id}", response_model=DraftResponse)
def getArticleDraft(
    draft_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> DraftResponse:
    draft = getDraft(int(currentUser["id"]), draft_id)
    if draft is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Draft not found")

    return DraftResponse(**draft)


@router.put("/drafts/{draft_id}", response_model=DraftResponse)
def updateArticleDraft(
    draft_id: int,
    request: DraftRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> DraftResponse:
    draft = updateDraft(
        int(currentUser["id"]),
        draft_id,
        request.title,
        request.summary,
        request.content,
        request.category_id,
        request.visible_type,
        request.tags,
    )
    if draft is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Draft not found")

    return DraftResponse(**draft)


@router.delete("/drafts/{draft_id}")
def deleteArticleDraft(
    draft_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    isDeleted = deleteDraft(int(currentUser["id"]), draft_id)
    if not isDeleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Draft not found")

    return {"status": "ok"}


@router.post("/drafts/{draft_id}/publish", response_model=DraftResponse)
def publishArticleDraft(
    draft_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> DraftResponse:
    article = publishDraft(int(currentUser["id"]), draft_id)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Draft not found")

    return DraftResponse(**article)


@router.post("/images")
def uploadArticleImage(
    image: UploadFile = File(...),
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    userId = int(currentUser["id"])
    imageUrl = _saveArticleImage(userId, image)

    with getDatabaseConnection() as connection:
        connection.execute(
            """
            INSERT INTO photos (user_id, url, source_type, visible_type)
            VALUES (?, ?, ?, ?)
            """,
            (userId, imageUrl, "article", "self"),
        )
        connection.commit()

    return {"url": imageUrl}


@router.get("/{article_id}", response_model=ArticleDetailResponse)
def getArticle(
    article_id: int,
    currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser),
) -> ArticleDetailResponse:
    userId = int(currentUser["id"]) if currentUser else None
    article = getVisibleArticle(article_id, userId)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    return ArticleDetailResponse(**article)


@router.get("/{article_id}/comments", response_model=CommentListResponse)
def getArticleComments(
    article_id: int,
    currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser),
) -> CommentListResponse:
    userId = int(currentUser["id"]) if currentUser else None
    if getVisibleArticle(article_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    return CommentListResponse(items=listComments(article_id, userId))


@router.post("/{article_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def createArticleComment(
    article_id: int,
    request: CommentRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> CommentResponse:
    userId = int(currentUser["id"])
    if getVisibleArticle(article_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    comment = createComment(userId, article_id, request.content, request.parent_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid parent comment")

    return CommentResponse(**comment)


@router.post("/{article_id}/comments/{comment_id}/likes", response_model=InteractionResponse)
def likeArticleCommentEndpoint(
    article_id: int,
    comment_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleArticle(article_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if getTargetComment(comment_id, "article", article_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    likeTarget(userId, "comment", comment_id)
    return InteractionResponse(status="ok")


@router.delete("/{article_id}/comments/{comment_id}/likes", response_model=InteractionResponse)
def unlikeArticleCommentEndpoint(
    article_id: int,
    comment_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleArticle(article_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if getTargetComment(comment_id, "article", article_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    unlikeTarget(userId, "comment", comment_id)
    return InteractionResponse(status="ok")


@router.post("/{article_id}/likes", response_model=InteractionResponse)
def likeArticleEndpoint(
    article_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleArticle(article_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    likeArticle(userId, article_id)
    return InteractionResponse(status="ok")


@router.delete("/{article_id}/likes", response_model=InteractionResponse)
def unlikeArticleEndpoint(
    article_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleArticle(article_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    unlikeArticle(userId, article_id)
    return InteractionResponse(status="ok")


@router.post("/{article_id}/collects", response_model=InteractionResponse)
def collectArticleEndpoint(
    article_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleArticle(article_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    collectArticle(userId, article_id)
    return InteractionResponse(status="ok")


@router.delete("/{article_id}/collects", response_model=InteractionResponse)
def uncollectArticleEndpoint(
    article_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleArticle(article_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    uncollectArticle(userId, article_id)
    return InteractionResponse(status="ok")
