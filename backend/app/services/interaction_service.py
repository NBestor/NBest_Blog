from app.db.database import getDatabaseConnection


def getTargetStats(targetType: str, targetId: int, userId: int | None = None) -> dict[str, int | bool]:
    with getDatabaseConnection() as connection:
        likeCount = connection.execute(
            """
            SELECT COUNT(*) AS count FROM like_records
            WHERE target_type = ? AND target_id = ?
            """,
            (targetType, targetId),
        ).fetchone()["count"]
        commentCount = connection.execute(
            "SELECT COUNT(*) AS count FROM comments WHERE target_type = ? AND target_id = ?",
            (targetType, targetId),
        ).fetchone()["count"]
        isLiked = False
        isCollected = False
        if userId is not None:
            isLiked = (
                connection.execute(
                    """
                    SELECT 1 FROM like_records
                    WHERE user_id = ? AND target_type = ? AND target_id = ?
                    """,
                    (userId, targetType, targetId),
                ).fetchone()
                is not None
            )
            if targetType == "article":
                isCollected = (
                    connection.execute(
                        "SELECT 1 FROM collects WHERE user_id = ? AND article_id = ?",
                        (userId, targetId),
                    ).fetchone()
                    is not None
                )

    return {
        "like_count": likeCount,
        "comment_count": commentCount,
        "is_liked": isLiked,
        "is_collected": isCollected,
    }


def getArticleStats(articleId: int, userId: int | None = None) -> dict[str, int | bool]:
    return getTargetStats("article", articleId, userId)


def getQuickPostStats(quickPostId: int, userId: int | None = None) -> dict[str, int | bool]:
    return getTargetStats("quick_post", quickPostId, userId)


def getCommentStats(commentId: int, userId: int | None = None) -> dict[str, int | bool]:
    with getDatabaseConnection() as connection:
        likeCount = connection.execute(
            """
            SELECT COUNT(*) AS count FROM like_records
            WHERE target_type = 'comment' AND target_id = ?
            """,
            (commentId,),
        ).fetchone()["count"]
        isLiked = False
        if userId is not None:
            isLiked = (
                connection.execute(
                    """
                    SELECT 1 FROM like_records
                    WHERE user_id = ? AND target_type = 'comment' AND target_id = ?
                    """,
                    (userId, commentId),
                ).fetchone()
                is not None
            )

    return {"like_count": likeCount, "is_liked": isLiked}


def commentExists(commentId: int) -> bool:
    with getDatabaseConnection() as connection:
        row = connection.execute("SELECT 1 FROM comments WHERE id = ?", (commentId,)).fetchone()
        return row is not None


def likeArticle(userId: int, articleId: int) -> None:
    likeTarget(userId, "article", articleId)


def unlikeArticle(userId: int, articleId: int) -> None:
    unlikeTarget(userId, "article", articleId)


def likeTarget(userId: int, targetType: str, targetId: int) -> None:
    with getDatabaseConnection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO like_records (user_id, target_type, target_id)
            VALUES (?, ?, ?)
            """,
            (userId, targetType, targetId),
        )
        connection.commit()


def unlikeTarget(userId: int, targetType: str, targetId: int) -> None:
    with getDatabaseConnection() as connection:
        connection.execute(
            """
            DELETE FROM like_records
            WHERE user_id = ? AND target_type = ? AND target_id = ?
            """,
            (userId, targetType, targetId),
        )
        connection.commit()


def collectArticle(userId: int, articleId: int) -> None:
    with getDatabaseConnection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO collects (user_id, article_id)
            VALUES (?, ?)
            """,
            (userId, articleId),
        )
        connection.commit()


def uncollectArticle(userId: int, articleId: int) -> None:
    with getDatabaseConnection() as connection:
        connection.execute(
            "DELETE FROM collects WHERE user_id = ? AND article_id = ?",
            (userId, articleId),
        )
        connection.commit()
