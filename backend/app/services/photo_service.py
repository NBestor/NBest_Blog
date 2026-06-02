from pathlib import Path
from sqlite3 import Row
from uuid import uuid4

from app.core.config import getSettings
from app.db.database import getDatabaseConnection


def canManagePhoto(row: Row, currentUserId: int | None = None, currentUserRole: str | None = None) -> bool:
    return currentUserRole == "admin" or (currentUserId is not None and row["user_id"] == currentUserId)


def formatPhoto(
    row: Row,
    currentUserId: int | None = None,
    currentUserRole: str | None = None,
) -> dict[str, str | int | bool]:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "author_nickname": row["author_nickname"],
        "url": row["url"],
        "source_type": row["source_type"],
        "visible_type": row["visible_type"],
        "upload_time": row["upload_time"],
        "can_manage": canManagePhoto(row, currentUserId, currentUserRole),
    }


def listVisiblePhotos(
    currentUserId: int | None,
    currentUserRole: str | None = None,
) -> list[dict[str, str | int | bool]]:
    with getDatabaseConnection() as connection:
        if currentUserRole == "admin":
            rows = connection.execute(
                """
                SELECT photos.*, users.nickname AS author_nickname
                FROM photos
                JOIN users ON users.id = photos.user_id
                ORDER BY photos.upload_time DESC, photos.id DESC
                """
            ).fetchall()
        elif currentUserId is None:
            rows = connection.execute(
                """
                SELECT photos.*, users.nickname AS author_nickname
                FROM photos
                JOIN users ON users.id = photos.user_id
                WHERE photos.visible_type = 'public'
                ORDER BY photos.upload_time DESC, photos.id DESC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT photos.*, users.nickname AS author_nickname
                FROM photos
                JOIN users ON users.id = photos.user_id
                WHERE photos.visible_type = 'public' OR photos.user_id = ?
                ORDER BY photos.upload_time DESC, photos.id DESC
                """,
                (currentUserId,),
            ).fetchall()

    return [formatPhoto(row, currentUserId, currentUserRole) for row in rows]


def listAdminPhotos(currentUserId: int, currentUserRole: str) -> list[dict[str, str | int | bool]]:
    return listVisiblePhotos(currentUserId, currentUserRole)


def createPhotoRecord(userId: int, url: str, sourceType: str, visibleType: str = "self") -> None:
    with getDatabaseConnection() as connection:
        connection.execute(
            """
            INSERT INTO photos (user_id, url, source_type, visible_type)
            VALUES (?, ?, ?, ?)
            """,
            (userId, url, sourceType, visibleType),
        )
        connection.commit()


def saveUploadedPhoto(userId: int, fileName: str, content: bytes, visibleType: str) -> str:
    suffix = Path(fileName or "photo.png").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        suffix = ".png"

    photoDir = getSettings().upload_dir / "photos" / str(userId)
    photoDir.mkdir(parents=True, exist_ok=True)
    photoPath = photoDir / f"{uuid4().hex}{suffix}"
    photoPath.write_bytes(content)
    photoUrl = f"/static/uploads/photos/{userId}/{photoPath.name}"
    createPhotoRecord(userId, photoUrl, "upload", visibleType)
    return photoUrl


def updatePhotoVisibleType(
    userId: int,
    userRole: str,
    photoId: int,
    visibleType: str,
) -> dict[str, str | int | bool] | None:
    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT photos.*, users.nickname AS author_nickname
            FROM photos
            JOIN users ON users.id = photos.user_id
            WHERE photos.id = ?
            """,
            (photoId,),
        ).fetchone()
        if row is None or not canManagePhoto(row, userId, userRole):
            return None

        connection.execute(
            """
            UPDATE photos
            SET visible_type = ?
            WHERE id = ?
            """,
            (visibleType, photoId),
        )
        connection.commit()
        row = connection.execute(
            """
            SELECT photos.*, users.nickname AS author_nickname
            FROM photos
            JOIN users ON users.id = photos.user_id
            WHERE photos.id = ?
            """,
            (photoId,),
        ).fetchone()

    return formatPhoto(row, userId, userRole) if row else None


def deletePhoto(userId: int, userRole: str, photoId: int) -> bool:
    with getDatabaseConnection() as connection:
        row = connection.execute(
            "SELECT * FROM photos WHERE id = ?",
            (photoId,),
        ).fetchone()
        if row is None or not canManagePhoto(row, userId, userRole):
            return False

        connection.execute("DELETE FROM photos WHERE id = ?", (photoId,))
        connection.commit()

    staticPrefix = "/static/uploads/"
    if row["url"].startswith(staticPrefix):
        relativePath = row["url"].replace("/static/", "", 1)
        staticDir = getSettings().static_dir.resolve()
        filePath = (staticDir / relativePath).resolve()
        try:
            filePath.relative_to(staticDir)
        except ValueError:
            return True

        if filePath.exists():
            filePath.unlink()

    return True
