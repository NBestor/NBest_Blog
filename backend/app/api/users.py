from io import BytesIO
from pathlib import Path

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.api.auth import getCurrentUser, getOptionalCurrentUser
from app.core.config import getSettings
from app.schemas.auth import UserResponse
from app.schemas.follow import FollowListResponse
from app.schemas.user import PasswordUpdateRequest, ProfileUpdateRequest
from app.services.photo_service import createPhotoRecord
from app.services.user_service import (
    getUserProfile,
    getUserSettings,
    listUsersWithRelation,
    updateUserAvatar,
    updateUserPassword,
    updateUserProfile,
    updateUserSettings,
)


router = APIRouter(prefix="/users", tags=["users"])


class UserSettingsRequest(BaseModel):
    quick_post_default_visible_type: str = Field(pattern="^(public|friend|self)$")


@router.get("", response_model=FollowListResponse)
def getUsers(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> FollowListResponse:
    return FollowListResponse(items=listUsersWithRelation(int(currentUser["id"])))


def _saveAvatar(userId: int, uploadFile: UploadFile) -> str:
    if uploadFile.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported image type")

    settings = getSettings()
    avatarDir = settings.upload_dir / "avatars" / str(userId)
    avatarDir.mkdir(parents=True, exist_ok=True)

    try:
        image = Image.open(BytesIO(uploadFile.file.read()))
        image = image.convert("RGB")
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file") from exc

    image.thumbnail((256, 256))
    canvas = Image.new("RGB", (256, 256), (245, 245, 245))
    left = (256 - image.width) // 2
    top = (256 - image.height) // 2
    canvas.paste(image, (left, top))

    avatarPath = avatarDir / "avatar.jpg"
    canvas.save(avatarPath, format="JPEG", quality=88)
    return f"/static/uploads/avatars/{userId}/{Path(avatarPath).name}"


@router.put("/me", response_model=UserResponse)
def updateMe(
    request: ProfileUpdateRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> UserResponse:
    user = updateUserProfile(int(currentUser["id"]), request.nickname, request.signature)
    return UserResponse(**user)


@router.get("/me/settings")
def getMeSettings(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> dict[str, str]:
    return getUserSettings(int(currentUser["id"]))


@router.put("/me/settings")
def updateMeSettings(
    request: UserSettingsRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    return updateUserSettings(int(currentUser["id"]), request.quick_post_default_visible_type)


@router.post("/me/avatar", response_model=UserResponse)
def uploadAvatar(
    avatar: UploadFile = File(...),
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> UserResponse:
    avatarUrl = _saveAvatar(int(currentUser["id"]), avatar)
    createPhotoRecord(int(currentUser["id"]), avatarUrl, "avatar", "self")
    user = updateUserAvatar(int(currentUser["id"]), avatarUrl)
    return UserResponse(**user)


@router.delete("/me/avatar", response_model=UserResponse)
def resetAvatar(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> UserResponse:
    userId = int(currentUser["id"])
    avatarPath = getSettings().upload_dir / "avatars" / str(userId) / "avatar.jpg"
    if avatarPath.exists():
        avatarPath.unlink()

    user = updateUserAvatar(userId, None)
    return UserResponse(**user)


@router.get("/{id}/profile")
def getUserPublicProfile(
    id: int,
    currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser),
):
    currentUserId = int(currentUser["id"]) if currentUser else None
    profile = getUserProfile(id, currentUserId)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return profile


@router.put("/me/password")
def updatePassword(
    request: PasswordUpdateRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    isUpdated = updateUserPassword(int(currentUser["id"]), request.old_password, request.new_password)
    if not isUpdated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    return {"status": "ok"}
