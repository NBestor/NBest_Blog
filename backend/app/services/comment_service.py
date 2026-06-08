import logging
import threading
from sqlite3 import Row

from app.core.config import getSettings
from app.core.timezone import toBeijingTime
from app.db.database import getDatabaseConnection
from app.services.interaction_service import getCommentStats

logger = logging.getLogger("app.services.comment")

NIUBAO_USER_ID = 666


def formatComment(row: Row, currentUserId: int | None = None) -> dict[str, str | int | bool | None | list]:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "article_id": row["article_id"],
        "parent_id": row["parent_id"],
        "author_nickname": row["author_nickname"],
        "content": row["content"],
        "create_time": toBeijingTime(row["create_time"]),
        **getCommentStats(row["id"], currentUserId),
        "children": [],
    }


def buildCommentTree(comments: list[dict[str, str | int | bool | None | list]]) -> list[dict]:
    commentById = {comment["id"]: comment for comment in comments}
    roots = []

    for comment in comments:
        parentId = comment["parent_id"]
        if parentId is not None and parentId in commentById:
            commentById[parentId]["children"].append(comment)
        else:
            roots.append(comment)

    return roots


def getTargetComment(commentId: int, targetType: str, targetId: int) -> Row | None:
    with getDatabaseConnection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM comments
            WHERE id = ? AND target_type = ? AND target_id = ?
            """,
            (commentId, targetType, targetId),
        ).fetchone()


def createComment(
    userId: int,
    articleId: int,
    content: str,
    parentId: int | None = None,
) -> dict[str, str | int | bool | None | list] | None:
    return createTargetComment(userId, "article", articleId, content, articleId, parentId)


def createTargetComment(
    userId: int,
    targetType: str,
    targetId: int,
    content: str,
    articleId: int | None = None,
    parentId: int | None = None,
) -> dict[str, str | int | bool | None | list] | None:
    with getDatabaseConnection() as connection:
        if parentId is not None:
            parentRow = connection.execute(
                """
                SELECT 1
                FROM comments
                WHERE id = ? AND target_type = ? AND target_id = ?
                """,
                (parentId, targetType, targetId),
            ).fetchone()
            if parentRow is None:
                return None

        cursor = connection.execute(
            """
            INSERT INTO comments (user_id, article_id, parent_id, target_type, target_id, content)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (userId, articleId, parentId, targetType, targetId, content),
        )
        connection.commit()
        newCommentId = cursor.lastrowid
        row = connection.execute(
            """
            SELECT comments.*, users.nickname AS author_nickname
            FROM comments
            JOIN users ON users.id = comments.user_id
            WHERE comments.id = ?
            """,
            (newCommentId,),
        ).fetchone()

    # Trigger Niubao auto-reply in background if replying to Niubao's comment
    if parentId is not None and userId != NIUBAO_USER_ID:
        threading.Thread(
            target=_maybeAutoReply,
            args=(userId, targetType, targetId, parentId, newCommentId, content),
            daemon=True,
        ).start()

    return formatComment(row, userId)


def _maybeAutoReply(
    userId: int,
    targetType: str,
    targetId: int,
    parentId: int,
    newCommentId: int,
    replyContent: str,
) -> None:
    """Check if parent comment is from Niubao and auto-reply in a background thread."""
    try:
        with getDatabaseConnection() as connection:
            parentCommentRow = connection.execute(
                "SELECT user_id, content FROM comments WHERE id = ?",
                (parentId,),
            ).fetchone()

        if parentCommentRow is None or parentCommentRow["user_id"] != NIUBAO_USER_ID:
            return

        parentComment = parentCommentRow["content"]

        # Get target content
        with getDatabaseConnection() as connection:
            if targetType == "article":
                targetRow = connection.execute(
                    "SELECT content FROM articles WHERE id = ?",
                    (targetId,),
                ).fetchone()
            else:
                targetRow = connection.execute(
                    "SELECT content FROM quick_posts WHERE id = ?",
                    (targetId,),
                ).fetchone()

        targetContent = targetRow["content"] if targetRow else ""
        if not targetContent:
            targetContent = f"（{targetType}: {targetId}）"

        settings = getSettings()
        from app.services.ai_service import generateReply

        reply = generateReply(
            targetContent=targetContent,
            parentComment=parentComment,
            replyContent=replyContent,
            api_key=settings.ai_api_key,
            base_url=settings.ai_base_url,
            model=settings.ai_model,
        )

        if reply is None:
            return

        createTargetComment(
            NIUBAO_USER_ID,
            targetType,
            targetId,
            reply,
            articleId=None if targetType != "article" else targetId,
            parentId=newCommentId,
        )

        logger.info(
            f"Niubao auto-reply created: parentId={newCommentId}, "
            f"targetType={targetType}, targetId={targetId}"
        )

    except Exception as e:
        logger.error(f"Niubao auto-reply background task failed: {e}")


def listComments(articleId: int, currentUserId: int | None = None) -> list[dict]:
    return listTargetComments("article", articleId, currentUserId)


def listTargetComments(targetType: str, targetId: int, currentUserId: int | None = None) -> list[dict]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT comments.*, users.nickname AS author_nickname
            FROM comments
            JOIN users ON users.id = comments.user_id
            WHERE comments.target_type = ? AND comments.target_id = ?
            ORDER BY comments.create_time ASC, comments.id ASC
            """,
            (targetType, targetId),
        ).fetchall()

    return buildCommentTree([formatComment(row, currentUserId) for row in rows])


def listAdminComments() -> list[dict[str, str | int | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT comments.*, users.nickname AS author_nickname
            FROM comments
            JOIN users ON users.id = comments.user_id
            ORDER BY comments.create_time DESC, comments.id DESC
            """
        ).fetchall()

    return [
        {
            **formatComment(row),
            "target_type": row["target_type"],
            "target_id": row["target_id"],
        }
        for row in rows
    ]


def deleteCommentByAdmin(commentId: int) -> bool:
    with getDatabaseConnection() as connection:
        cursor = connection.execute("DELETE FROM comments WHERE id = ?", (commentId,))
        connection.commit()
        return cursor.rowcount > 0
