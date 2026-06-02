from sqlite3 import IntegrityError, Row

from app.core.config import getSettings
from app.core.security import getPasswordHash, verifyPassword
from app.db.database import getDatabaseConnection


def formatUser(row: Row) -> dict[str, str | int | None]:
    return {
        "id": row["id"],
        "username": row["username"],
        "nickname": row["nickname"],
        "avatar_url": row["avatar_url"],
        "signature": row["signature"],
        "role": row["role"],
        "create_time": row["create_time"],
    }


def isSupervisorUser(user: dict[str, str | int | None]) -> bool:
    return user.get("id") == 0 and user.get("username") == "NBest" and user.get("role") == "admin"


def canManageUser(
    actor: dict[str, str | int | None],
    target: Row | dict[str, str | int | None],
) -> bool:
    targetId = int(target["id"])
    targetRole = str(target["role"])

    if targetId == 0:
        return False

    if isSupervisorUser(actor):
        return int(actor["id"]) != targetId

    return actor.get("role") == "admin" and targetRole == "user" and int(actor["id"]) != targetId


def formatAdminUser(row: Row, actor: dict[str, str | int | None]) -> dict[str, str | int | bool | None]:
    return {
        **formatUser(row),
        "has_avatar": bool(row["avatar_url"]),
        "is_supervisor": row["id"] == 0 and row["username"] == "NBest",
        "can_manage": canManageUser(actor, row),
        "can_change_role": isSupervisorUser(actor) and row["id"] != 0 and int(actor["id"]) != row["id"],
    }


def getUserByUsername(username: str) -> Row | None:
    with getDatabaseConnection() as connection:
        return connection.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def getUserById(userId: int) -> Row | None:
    with getDatabaseConnection() as connection:
        return connection.execute("SELECT * FROM users WHERE id = ?", (userId,)).fetchone()


def listAdminUsers(actor: dict[str, str | int | None]) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM users
            ORDER BY
                CASE WHEN id = 0 THEN 0 ELSE 1 END,
                role ASC,
                create_time DESC,
                id DESC
            """
        ).fetchall()

    return [formatAdminUser(row, actor) for row in rows]


def deleteAdminUser(actor: dict[str, str | int | None], targetUserId: int) -> bool:
    with getDatabaseConnection() as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (targetUserId,)).fetchone()
        if row is None or not canManageUser(actor, row):
            return False

        connection.execute("DELETE FROM users WHERE id = ?", (targetUserId,))
        connection.commit()
        return True


def forceRenameUser(
    actor: dict[str, str | int | None],
    targetUserId: int,
    replacementName: str | None = None,
) -> dict[str, str | int | bool | None] | None:
    with getDatabaseConnection() as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (targetUserId,)).fetchone()
        if row is None or not canManageUser(actor, row):
            return None

        safeName = replacementName.strip() if replacementName else f"user_{targetUserId}"
        if not safeName:
            safeName = f"user_{targetUserId}"
        safeName = safeName[:32]
        connection.execute(
            """
            UPDATE users
            SET username = ?, nickname = ?
            WHERE id = ?
            """,
            (safeName, safeName, targetUserId),
        )
        connection.commit()
        row = connection.execute("SELECT * FROM users WHERE id = ?", (targetUserId,)).fetchone()

    return formatAdminUser(row, actor) if row else None


def removeUserAvatarByAdmin(
    actor: dict[str, str | int | None],
    targetUserId: int,
) -> dict[str, str | int | bool | None] | None:
    with getDatabaseConnection() as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (targetUserId,)).fetchone()
        if row is None or not canManageUser(actor, row):
            return None

        avatarUrl = row["avatar_url"]
        connection.execute("UPDATE users SET avatar_url = NULL WHERE id = ?", (targetUserId,))
        connection.commit()
        row = connection.execute("SELECT * FROM users WHERE id = ?", (targetUserId,)).fetchone()

    staticPrefix = "/static/uploads/"
    if avatarUrl and avatarUrl.startswith(staticPrefix):
        relativePath = avatarUrl.replace("/static/", "", 1)
        staticDir = getSettings().static_dir.resolve()
        filePath = (staticDir / relativePath).resolve()
        try:
            filePath.relative_to(staticDir)
        except ValueError:
            return formatAdminUser(row, actor) if row else None

        if filePath.exists():
            filePath.unlink()

    return formatAdminUser(row, actor) if row else None


def updateUserRoleBySupervisor(
    actor: dict[str, str | int | None],
    targetUserId: int,
    role: str,
) -> dict[str, str | int | bool | None] | None:
    if not isSupervisorUser(actor) or role not in {"user", "admin"} or targetUserId == 0:
        return None

    with getDatabaseConnection() as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (targetUserId,)).fetchone()
        if row is None or int(actor["id"]) == targetUserId:
            return None

        connection.execute("UPDATE users SET role = ? WHERE id = ?", (role, targetUserId))
        connection.commit()
        row = connection.execute("SELECT * FROM users WHERE id = ?", (targetUserId,)).fetchone()

    return formatAdminUser(row, actor) if row else None


def createUser(username: str, password: str, nickname: str) -> dict[str, str | int | None] | None:
    with getDatabaseConnection() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO users (username, password_hash, nickname, role)
                VALUES (?, ?, ?, ?)
                """,
                (username, getPasswordHash(password), nickname, "user"),
            )
            connection.commit()
        except IntegrityError:
            return None

        row = connection.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return formatUser(row)


def authenticateUser(username: str, password: str) -> dict[str, str | int | None] | None:
    row = getUserByUsername(username)
    if row is None or not verifyPassword(password, row["password_hash"]):
        return None

    return formatUser(row)


def listUsersWithRelation(currentUserId: int) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT
                users.*,
                CASE WHEN current_follow.id IS NULL THEN 0 ELSE 1 END AS is_following,
                CASE WHEN friend_follow.id IS NULL THEN 0 ELSE 1 END AS is_friend
            FROM users
            LEFT JOIN follows AS current_follow
                ON current_follow.user_id = ?
                AND current_follow.follow_user_id = users.id
            LEFT JOIN follows AS friend_follow
                ON friend_follow.user_id = users.id
                AND friend_follow.follow_user_id = ?
            WHERE users.id != ?
            ORDER BY users.create_time DESC, users.id DESC
            """,
            (currentUserId, currentUserId, currentUserId),
        ).fetchall()

    return [
        {
            **formatUser(row),
            "is_following": bool(row["is_following"]),
            "is_friend": bool(row["is_following"] and row["is_friend"]),
        }
        for row in rows
    ]


def updateUserProfile(userId: int, nickname: str, signature: str | None) -> dict[str, str | int | None]:
    with getDatabaseConnection() as connection:
        connection.execute(
            """
            UPDATE users
            SET nickname = ?, signature = ?
            WHERE id = ?
            """,
            (nickname, signature, userId),
        )
        connection.commit()
        row = connection.execute("SELECT * FROM users WHERE id = ?", (userId,)).fetchone()
        return formatUser(row)


def updateUserAvatar(userId: int, avatarUrl: str | None) -> dict[str, str | int | None]:
    with getDatabaseConnection() as connection:
        connection.execute("UPDATE users SET avatar_url = ? WHERE id = ?", (avatarUrl, userId))
        connection.commit()
        row = connection.execute("SELECT * FROM users WHERE id = ?", (userId,)).fetchone()
        return formatUser(row)


def updateUserPassword(userId: int, oldPassword: str, newPassword: str) -> bool:
    with getDatabaseConnection() as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (userId,)).fetchone()
        if row is None or not verifyPassword(oldPassword, row["password_hash"]):
            return False

        connection.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (getPasswordHash(newPassword), userId),
        )
        connection.commit()
        return True


def getUserSettings(userId: int) -> dict[str, str]:
    with getDatabaseConnection() as connection:
        row = connection.execute(
            "SELECT quick_post_default_visible_type FROM users WHERE id = ?",
            (userId,),
        ).fetchone()
    return {"quick_post_default_visible_type": row["quick_post_default_visible_type"]}


def updateUserSettings(userId: int, quickPostDefaultVisibleType: str) -> dict[str, str]:
    with getDatabaseConnection() as connection:
        connection.execute(
            "UPDATE users SET quick_post_default_visible_type = ? WHERE id = ?",
            (quickPostDefaultVisibleType, userId),
        )
        connection.commit()
    return getUserSettings(userId)
