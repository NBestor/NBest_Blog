import re

from app.db.database import getDatabaseConnection
from app.services.article_category_service import canUseCategory
from app.services.article_tag_service import getArticleTags, syncArticleTags
from app.services.interaction_service import getArticleStats


SUMMARY_LIMIT = 300


def buildArticleSummary(summary: str | None, content: str) -> str | None:
    source = summary.strip() if summary else ""
    if not source:
        source = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", content)
        source = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", source)
        source = re.sub(r"[#>*_`~$\\-]+", " ", source)
        source = re.sub(r"\s+", " ", source).strip()
    if not source:
        return None
    return source[:SUMMARY_LIMIT]


def formatArticle(row: Row) -> dict[str, str | int | bool | None]:
    article = {
        "id": row["id"],
        "user_id": row["user_id"],
        "title": row["title"],
        "summary": buildArticleSummary(row["summary"], row["content"]),
        "content": row["content"],
        "is_draft": bool(row["is_draft"]),
        "category_id": row["category_id"],
        "category_name": row["category_name"] if "category_name" in row.keys() else None,
        "visible_type": row["visible_type"],
        "tags": getArticleTags(row["id"]),
        "create_time": row["create_time"],
        "update_time": row["update_time"],
    }
    return article


def isFriend(userId: int, otherUserId: int) -> bool:
    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT 1
            FROM follows AS a
            JOIN follows AS b
                ON b.user_id = a.follow_user_id
                AND b.follow_user_id = a.user_id
            WHERE a.user_id = ? AND a.follow_user_id = ?
            """,
            (userId, otherUserId),
        ).fetchone()

    return row is not None


def canViewArticle(row: Row, currentUserId: int | None) -> bool:
    if row["visible_type"] == "public":
        return True

    if currentUserId is None:
        return False

    if row["user_id"] == currentUserId:
        return True

    if row["visible_type"] == "friend":
        return isFriend(currentUserId, row["user_id"])

    return False


def formatReadableArticle(row: Row, currentUserId: int | None) -> dict[str, str | int | bool | None]:
    return {
        **formatArticle(row),
        "author_nickname": row["author_nickname"],
        **getArticleStats(row["id"], currentUserId),
    }


def createDraft(
    userId: int,
    title: str,
    summary: str | None,
    content: str,
    categoryId: int | None,
    visibleType: str,
    tags: list[str],
) -> dict[str, str | int | bool | None] | None:
    if not canUseCategory(userId, categoryId):
        return None

    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO articles (user_id, title, summary, content, is_draft, category_id, visible_type)
            VALUES (?, ?, ?, ?, 1, ?, ?)
            """,
            (userId, title, summary, content, categoryId, visibleType),
        )
        connection.commit()
        articleId = cursor.lastrowid

    syncArticleTags(userId, articleId, tags)
    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT articles.*, article_categories.name AS category_name
            FROM articles
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            WHERE articles.id = ?
            """,
            (articleId,),
        ).fetchone()
        return formatArticle(row)


def listDrafts(userId: int) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT articles.*, article_categories.name AS category_name
            FROM articles
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            WHERE articles.user_id = ? AND articles.is_draft = 1
            ORDER BY articles.update_time DESC, articles.id DESC
            """,
            (userId,),
        ).fetchall()

    return [formatArticle(row) for row in rows]


def getDraft(userId: int, draftId: int) -> dict[str, str | int | bool | None] | None:
    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT articles.*, article_categories.name AS category_name
            FROM articles
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            WHERE articles.id = ? AND articles.user_id = ? AND articles.is_draft = 1
            """,
            (draftId, userId),
        ).fetchone()

    return formatArticle(row) if row else None


def updateDraft(
    userId: int,
    draftId: int,
    title: str,
    summary: str | None,
    content: str,
    categoryId: int | None,
    visibleType: str,
    tags: list[str],
) -> dict[str, str | int | bool | None] | None:
    if not canUseCategory(userId, categoryId):
        return None

    with getDatabaseConnection() as connection:
        connection.execute(
            """
            UPDATE articles
            SET title = ?, summary = ?, content = ?, category_id = ?, visible_type = ?, update_time = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ? AND is_draft = 1
            """,
            (title, summary, content, categoryId, visibleType, draftId, userId),
        )
        connection.commit()

    syncArticleTags(userId, draftId, tags)

    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT articles.*, article_categories.name AS category_name
            FROM articles
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            WHERE articles.id = ? AND articles.user_id = ? AND articles.is_draft = 1
            """,
            (draftId, userId),
        ).fetchone()

    return formatArticle(row) if row else None


def deleteDraft(userId: int, draftId: int) -> bool:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM articles
            WHERE id = ? AND user_id = ? AND is_draft = 1
            """,
            (draftId, userId),
        )
        connection.commit()
        return cursor.rowcount > 0


def publishDraft(userId: int, draftId: int) -> dict[str, str | int | bool | None] | None:
    with getDatabaseConnection() as connection:
        connection.execute(
            """
            UPDATE articles
            SET is_draft = 0, update_time = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ? AND is_draft = 1
            """,
            (draftId, userId),
        )
        connection.commit()
        row = connection.execute(
            """
            SELECT articles.*, article_categories.name AS category_name
            FROM articles
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            WHERE articles.id = ? AND articles.user_id = ?
            """,
            (draftId, userId),
        ).fetchone()

    return formatArticle(row) if row else None


def updatePublishedArticle(
    userId: int,
    articleId: int,
    title: str,
    summary: str | None,
    content: str,
    categoryId: int | None,
    visibleType: str,
    tags: list[str],
) -> dict[str, str | int | bool | None] | None:
    if not canUseCategory(userId, categoryId):
        return None

    with getDatabaseConnection() as connection:
        row = connection.execute(
            "SELECT id, user_id FROM articles WHERE id = ? AND is_draft = 0",
            (articleId,),
        ).fetchone()

    if row is None or row["user_id"] != userId:
        return None

    with getDatabaseConnection() as connection:
        connection.execute(
            """
            UPDATE articles
            SET title = ?, summary = ?, content = ?, category_id = ?,
                visible_type = ?, update_time = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ? AND is_draft = 0
            """,
            (title, summary, content, categoryId, visibleType, articleId, userId),
        )
        connection.commit()

    syncArticleTags(userId, articleId, tags)

    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT articles.*, article_categories.name AS category_name
            FROM articles
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            WHERE articles.id = ?
            """,
            (articleId,),
        ).fetchone()

    return formatArticle(row) if row else None


def listVisibleArticles(currentUserId: int | None) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT
                articles.*,
                article_categories.name AS category_name,
                users.nickname AS author_nickname
            FROM articles
            JOIN users ON users.id = articles.user_id
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            WHERE articles.is_draft = 0
            ORDER BY articles.update_time DESC, articles.id DESC
            """
        ).fetchall()

    return [formatReadableArticle(row, currentUserId) for row in rows if canViewArticle(row, currentUserId)]


def articleMatchesQuery(article: dict[str, str | int | bool | None], query: str) -> bool:
    normalizedQuery = query.strip().lower()
    if not normalizedQuery:
        return False

    fields = [
        str(article.get("title") or ""),
        str(article.get("summary") or ""),
        str(article.get("category_name") or ""),
        " ".join(str(tag) for tag in article.get("tags", [])),
    ]
    return any(normalizedQuery in field.lower() for field in fields)


def searchVisibleArticles(query: str, currentUserId: int | None) -> list[dict[str, str | int | bool | None]]:
    if not query.strip():
        return []

    return [article for article in listVisibleArticles(currentUserId) if articleMatchesQuery(article, query)]


def getVisibleArticle(articleId: int, currentUserId: int | None) -> dict[str, str | int | bool | None] | None:
    with getDatabaseConnection() as connection:
        row = connection.execute(
            """
            SELECT
                articles.*,
                article_categories.name AS category_name,
                users.nickname AS author_nickname
            FROM articles
            JOIN users ON users.id = articles.user_id
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            WHERE articles.id = ? AND articles.is_draft = 0
            """,
            (articleId,),
        ).fetchone()

    if row is None or not canViewArticle(row, currentUserId):
        return None

    return formatReadableArticle(row, currentUserId)


def listAdminArticles() -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT
                articles.*,
                article_categories.name AS category_name,
                users.nickname AS author_nickname
            FROM articles
            JOIN users ON users.id = articles.user_id
            LEFT JOIN article_categories ON article_categories.id = articles.category_id
            ORDER BY articles.update_time DESC, articles.id DESC
            """
        ).fetchall()

    return [
        {
            **formatArticle(row),
            "author_nickname": row["author_nickname"],
        }
        for row in rows
    ]


def deleteArticleByAdmin(articleId: int) -> bool:
    with getDatabaseConnection() as connection:
        cursor = connection.execute("DELETE FROM articles WHERE id = ?", (articleId,))
        connection.commit()
        return cursor.rowcount > 0
