from sqlite3 import Row

from app.db.database import getDatabaseConnection
from app.services.article_service import isFriend
from app.services.interaction_service import getQuickPostStats


def canViewQuickPost(row: Row, currentUserId: int | None) -> bool:
    if row["visible_type"] == "public":
        return True
    if currentUserId is None:
        return False
    if row["user_id"] == currentUserId:
        return True
    if row["visible_type"] == "friend":
        return isFriend(currentUserId, row["user_id"])
    return False


def formatQuickPost(row: Row, currentUserId: int | None) -> dict[str, str | int | bool]:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "author_nickname": row["author_nickname"],
        "content": row["content"],
        "visible_type": row["visible_type"],
        "create_time": row["create_time"],
        "update_time": row["update_time"],
        "can_manage": currentUserId is not None and row["user_id"] == currentUserId,
        **getQuickPostStats(row["id"], currentUserId),
    }


def listVisibleQuickPosts(currentUserId: int | None) -> list[dict[str, str | int | bool]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT quick_posts.*, users.nickname AS author_nickname
            FROM quick_posts
            JOIN users ON users.id = quick_posts.user_id
            ORDER BY quick_posts.update_time DESC, quick_posts.id DESC
            """
        ).fetchall()

    return [formatQuickPost(row, currentUserId) for row in rows if canViewQuickPost(row, currentUserId)]


def searchVisibleQuickPosts(query: str, currentUserId: int | None) -> list[dict[str, str | int | bool]]:
    normalizedQuery = query.strip().lower()
    if not normalizedQuery:
        return []

    return [
        post
        for post in listVisibleQuickPosts(currentUserId)
        if normalizedQuery in str(post["content"]).lower()
    ]


def getVisibleQuickPost(quickPostId: int, currentUserId: int | None) -> dict[str, str | int | bool] | None:
    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT quick_posts.*, users.nickname AS author_nickname
            FROM quick_posts
            JOIN users ON users.id = quick_posts.user_id
            WHERE quick_posts.id = ?
            """,
            (quickPostId,),
        ).fetchone()

    if row is None or not canViewQuickPost(row, currentUserId):
        return None

    return formatQuickPost(row, currentUserId)


def createQuickPost(userId: int, content: str, visibleType: str | None) -> dict[str, str | int | bool]:
    with getDatabaseConnection() as connection:
        if visibleType is None:
            visibleType = connection.execute(
                "SELECT quick_post_default_visible_type FROM users WHERE id = ?",
                (userId,),
            ).fetchone()["quick_post_default_visible_type"]
        cursor = connection.execute(
            """
            INSERT INTO quick_posts (user_id, content, visible_type)
            VALUES (?, ?, ?)
            """,
            (userId, content, visibleType),
        )
        connection.commit()
        row = connection.execute(
            """
            SELECT quick_posts.*, users.nickname AS author_nickname
            FROM quick_posts
            JOIN users ON users.id = quick_posts.user_id
            WHERE quick_posts.id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return formatQuickPost(row, userId)


def deleteQuickPost(userId: int, quickPostId: int) -> bool:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            "DELETE FROM quick_posts WHERE id = ? AND user_id = ?",
            (quickPostId, userId),
        )
        connection.commit()
        return cursor.rowcount > 0


def updateQuickPost(userId: int, quickPostId: int, content: str, visibleType: str) -> dict[str, str | int | bool] | None:
    with getDatabaseConnection() as connection:
        row = connection.execute(
            "SELECT id, user_id FROM quick_posts WHERE id = ?",
            (quickPostId,),
        ).fetchone()

    if row is None or row["user_id"] != userId:
        return None

    with getDatabaseConnection() as connection:
        connection.execute(
            "UPDATE quick_posts SET content = ?, visible_type = ?, update_time = CURRENT_TIMESTAMP WHERE id = ?",
            (content, visibleType, quickPostId),
        )
        connection.commit()
        row = connection.execute(
            """
            SELECT quick_posts.*, users.nickname AS author_nickname
            FROM quick_posts
            JOIN users ON users.id = quick_posts.user_id
            WHERE quick_posts.id = ?
            """,
            (quickPostId,),
        ).fetchone()

    return formatQuickPost(row, userId)


def listAdminQuickPosts() -> list[dict[str, str | int | bool]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT quick_posts.*, users.nickname AS author_nickname
            FROM quick_posts
            JOIN users ON users.id = quick_posts.user_id
            ORDER BY quick_posts.update_time DESC, quick_posts.id DESC
            """
        ).fetchall()

    return [formatQuickPost(row, None) for row in rows]


def deleteQuickPostByAdmin(quickPostId: int) -> bool:
    with getDatabaseConnection() as connection:
        cursor = connection.execute("DELETE FROM quick_posts WHERE id = ?", (quickPostId,))
        connection.commit()
        return cursor.rowcount > 0
