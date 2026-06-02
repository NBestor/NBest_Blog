from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth import getCurrentAdmin, getCurrentSupervisor
from app.db.database import getDatabaseConnection
from app.schemas.admin import (
    AdminArticleListResponse,
    AdminCommentListResponse,
    AdminQuickPostListResponse,
    AdminRenameRequest,
    AdminRoleRequest,
    AdminSummaryResponse,
    AdminUserListResponse,
    AdminUserResponse,
)
from app.schemas.photo import PhotoListResponse
from app.services.article_service import deleteArticleByAdmin, listAdminArticles
from app.services.comment_service import deleteCommentByAdmin, listAdminComments
from app.services.photo_service import deletePhoto, listAdminPhotos
from app.services.quick_post_service import deleteQuickPostByAdmin, listAdminQuickPosts
from app.services.user_service import (
    deleteAdminUser,
    forceRenameUser,
    listAdminUsers,
    removeUserAvatarByAdmin,
    updateUserRoleBySupervisor,
)


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/summary", response_model=AdminSummaryResponse)
def getAdminSummary(
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> AdminSummaryResponse:
    del currentAdmin
    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM users) AS users,
                (SELECT COUNT(*) FROM users WHERE role = 'admin') AS admins,
                (SELECT COUNT(*) FROM articles) AS articles,
                (SELECT COUNT(*) FROM quick_posts) AS quick_posts,
                (SELECT COUNT(*) FROM comments) AS comments,
                (SELECT COUNT(*) FROM photos) AS photos
            """
        ).fetchone()

    return AdminSummaryResponse(**dict(row))


@router.get("/users", response_model=AdminUserListResponse)
def getAdminUsers(
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> AdminUserListResponse:
    return AdminUserListResponse(items=listAdminUsers(currentAdmin))


@router.delete("/users/{user_id}")
def deleteUserByAdmin(
    user_id: int,
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> dict[str, str]:
    if not deleteAdminUser(currentAdmin, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or not manageable")
    return {"status": "ok"}


@router.patch("/users/{user_id}/rename", response_model=AdminUserResponse)
def renameUserByAdmin(
    user_id: int,
    request: AdminRenameRequest,
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> AdminUserResponse:
    user = forceRenameUser(currentAdmin, user_id, request.name)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or not manageable")
    return AdminUserResponse(**user)


@router.delete("/users/{user_id}/avatar", response_model=AdminUserResponse)
def deleteUserAvatarByAdmin(
    user_id: int,
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> AdminUserResponse:
    user = removeUserAvatarByAdmin(currentAdmin, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or not manageable")
    return AdminUserResponse(**user)


@router.patch("/users/{user_id}/role", response_model=AdminUserResponse)
def updateUserRoleByAdmin(
    user_id: int,
    request: AdminRoleRequest,
    currentSupervisor: dict[str, str | int | None] = Depends(getCurrentSupervisor),
) -> AdminUserResponse:
    user = updateUserRoleBySupervisor(currentSupervisor, user_id, request.role)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or role not manageable")
    return AdminUserResponse(**user)


@router.get("/articles", response_model=AdminArticleListResponse)
def getAdminArticles(
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> AdminArticleListResponse:
    del currentAdmin
    return AdminArticleListResponse(items=listAdminArticles())


@router.delete("/articles/{article_id}")
def deleteArticleAdmin(
    article_id: int,
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> dict[str, str]:
    del currentAdmin
    if not deleteArticleByAdmin(article_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return {"status": "ok"}


@router.get("/quick-posts", response_model=AdminQuickPostListResponse)
def getAdminQuickPosts(
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> AdminQuickPostListResponse:
    del currentAdmin
    return AdminQuickPostListResponse(items=listAdminQuickPosts())


@router.delete("/quick-posts/{quick_post_id}")
def deleteQuickPostAdmin(
    quick_post_id: int,
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> dict[str, str]:
    del currentAdmin
    if not deleteQuickPostByAdmin(quick_post_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick post not found")
    return {"status": "ok"}


@router.get("/comments", response_model=AdminCommentListResponse)
def getAdminComments(
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> AdminCommentListResponse:
    del currentAdmin
    return AdminCommentListResponse(items=listAdminComments())


@router.delete("/comments/{comment_id}")
def deleteCommentAdmin(
    comment_id: int,
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> dict[str, str]:
    del currentAdmin
    if not deleteCommentByAdmin(comment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return {"status": "ok"}


@router.get("/photos", response_model=PhotoListResponse)
def getAdminPhotos(
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> PhotoListResponse:
    return PhotoListResponse(items=listAdminPhotos(int(currentAdmin["id"]), str(currentAdmin["role"])))


@router.delete("/photos/{photo_id}")
def deletePhotoAdmin(
    photo_id: int,
    currentAdmin: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> dict[str, str]:
    if not deletePhoto(int(currentAdmin["id"]), str(currentAdmin["role"]), photo_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return {"status": "ok"}
