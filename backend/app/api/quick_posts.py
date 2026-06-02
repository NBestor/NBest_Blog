from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth import getCurrentUser, getOptionalCurrentUser
from app.schemas.comment import CommentListResponse, CommentRequest, CommentResponse
from app.schemas.interaction import InteractionResponse
from app.schemas.quick_post import QuickPostListResponse, QuickPostRequest, QuickPostResponse
from app.services.comment_service import createTargetComment, getTargetComment, listTargetComments
from app.services.interaction_service import likeTarget, unlikeTarget
from app.services.quick_post_service import createQuickPost, deleteQuickPost, getVisibleQuickPost, listVisibleQuickPosts, updateQuickPost


router = APIRouter(prefix="/quick-posts", tags=["quick-posts"])


@router.get("", response_model=QuickPostListResponse)
def getQuickPosts(
    currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser),
) -> QuickPostListResponse:
    userId = int(currentUser["id"]) if currentUser else None
    return QuickPostListResponse(items=listVisibleQuickPosts(userId))


@router.post("", response_model=QuickPostResponse, status_code=status.HTTP_201_CREATED)
def createQuickPostEndpoint(
    request: QuickPostRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> QuickPostResponse:
    return QuickPostResponse(**createQuickPost(int(currentUser["id"]), request.content, request.visible_type))


@router.get("/{quick_post_id}", response_model=QuickPostResponse)
def getQuickPost(
    quick_post_id: int,
    currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser),
) -> QuickPostResponse:
    userId = int(currentUser["id"]) if currentUser else None
    quickPost = getVisibleQuickPost(quick_post_id, userId)
    if quickPost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    return QuickPostResponse(**quickPost)


@router.delete("/{quick_post_id}")
def deleteQuickPostEndpoint(
    quick_post_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    isDeleted = deleteQuickPost(int(currentUser["id"]), quick_post_id)
    if not isDeleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    return {"status": "ok"}


@router.put("/{quick_post_id}", response_model=QuickPostResponse)
def updateQuickPostEndpoint(
    quick_post_id: int,
    request: QuickPostRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> QuickPostResponse:
    userId = int(currentUser["id"])
    result = updateQuickPost(userId, quick_post_id, request.content, request.visible_type or "public")
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found or not authorized")
    return QuickPostResponse(**result)


@router.get("/{quick_post_id}/comments", response_model=CommentListResponse)
def getQuickPostComments(
    quick_post_id: int,
    currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser),
) -> CommentListResponse:
    userId = int(currentUser["id"]) if currentUser else None
    if getVisibleQuickPost(quick_post_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    return CommentListResponse(items=listTargetComments("quick_post", quick_post_id, userId))


@router.post("/{quick_post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def createQuickPostComment(
    quick_post_id: int,
    request: CommentRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> CommentResponse:
    userId = int(currentUser["id"])
    if getVisibleQuickPost(quick_post_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    comment = createTargetComment(userId, "quick_post", quick_post_id, request.content, None, request.parent_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid parent comment")

    return CommentResponse(**comment)


@router.post("/{quick_post_id}/comments/{comment_id}/likes", response_model=InteractionResponse)
def likeQuickPostComment(
    quick_post_id: int,
    comment_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleQuickPost(quick_post_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    if getTargetComment(comment_id, "quick_post", quick_post_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    likeTarget(userId, "comment", comment_id)
    return InteractionResponse(status="ok")


@router.delete("/{quick_post_id}/comments/{comment_id}/likes", response_model=InteractionResponse)
def unlikeQuickPostComment(
    quick_post_id: int,
    comment_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleQuickPost(quick_post_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    if getTargetComment(comment_id, "quick_post", quick_post_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    unlikeTarget(userId, "comment", comment_id)
    return InteractionResponse(status="ok")


@router.post("/{quick_post_id}/likes", response_model=InteractionResponse)
def likeQuickPost(
    quick_post_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleQuickPost(quick_post_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    likeTarget(userId, "quick_post", quick_post_id)
    return InteractionResponse(status="ok")


@router.delete("/{quick_post_id}/likes", response_model=InteractionResponse)
def unlikeQuickPost(
    quick_post_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> InteractionResponse:
    userId = int(currentUser["id"])
    if getVisibleQuickPost(quick_post_id, userId) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    unlikeTarget(userId, "quick_post", quick_post_id)
    return InteractionResponse(status="ok")
