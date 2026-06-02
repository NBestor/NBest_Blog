from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.api.auth import getCurrentUser, getOptionalCurrentUser
from app.schemas.photo import PhotoListResponse, PhotoResponse, PhotoUpdateRequest
from app.services.photo_service import deletePhoto, listVisiblePhotos, saveUploadedPhoto, updatePhotoVisibleType


router = APIRouter(prefix="/photos", tags=["photos"])


def _readImage(uploadFile: UploadFile) -> bytes:
    if uploadFile.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported image type")

    content = uploadFile.file.read()
    try:
        image = Image.open(BytesIO(content))
        image.verify()
    except (OSError, SyntaxError, UnidentifiedImageError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file") from exc

    return content


@router.get("", response_model=PhotoListResponse)
def getPhotos(currentUser: dict[str, str | int | None] | None = Depends(getOptionalCurrentUser)) -> PhotoListResponse:
    userId = int(currentUser["id"]) if currentUser else None
    userRole = str(currentUser["role"]) if currentUser else None
    return PhotoListResponse(items=listVisiblePhotos(userId, userRole))


@router.post("", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
def uploadPhoto(
    image: UploadFile = File(...),
    visible_type: str = Form("self"),
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> PhotoResponse:
    if visible_type not in {"public", "self"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid visible type")

    userId = int(currentUser["id"])
    imageUrl = saveUploadedPhoto(userId, image.filename or "photo.png", _readImage(image), visible_type)
    photos = listVisiblePhotos(userId, str(currentUser["role"]))
    photo = next(item for item in photos if item["url"] == imageUrl)
    return PhotoResponse(**photo)


@router.put("/{photo_id}", response_model=PhotoResponse)
def updatePhoto(
    photo_id: int,
    request: PhotoUpdateRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> PhotoResponse:
    photo = updatePhotoVisibleType(int(currentUser["id"]), str(currentUser["role"]), photo_id, request.visible_type)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    return PhotoResponse(**photo)


@router.delete("/{photo_id}")
def deletePhotoEndpoint(
    photo_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    isDeleted = deletePhoto(int(currentUser["id"]), str(currentUser["role"]), photo_id)
    if not isDeleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    return {"status": "ok"}
