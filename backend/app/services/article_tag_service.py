from sqlite3 import Row

from app.db.database import getDatabaseConnection


def formatTag(row: Row) -> dict[str, str | int]:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "name": row["name"],
        "create_time": row["create_time"],
    }


def normalizeTags(tags: list[str]) -> list[str]:
    normalizedTags = []
    seenNames = set()

    for tag in tags:
        tagName = tag.strip()
        if not tagName or tagName in seenNames:
            continue

        normalizedTags.append(tagName[:40])
        seenNames.add(tagName)

    return normalizedTags[:12]


def listTags(userId: int) -> list[dict[str, str | int]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM article_tags
            WHERE user_id = ?
            ORDER BY create_time DESC, id DESC
            """,
            (userId,),
        ).fetchall()

    return [formatTag(row) for row in rows]


def syncArticleTags(userId: int, articleId: int, tags: list[str]) -> None:
    tagNames = normalizeTags(tags)

    with getDatabaseConnection() as connection:
        connection.execute("DELETE FROM article_tag_relations WHERE article_id = ?", (articleId,))

        for tagName in tagNames:
            connection.execute(
                """
                INSERT OR IGNORE INTO article_tags (user_id, name)
                VALUES (?, ?)
                """,
                (userId, tagName),
            )
            tagRow = connection.execute(
                "SELECT id FROM article_tags WHERE user_id = ? AND name = ?",
                (userId, tagName),
            ).fetchone()
            connection.execute(
                """
                INSERT OR IGNORE INTO article_tag_relations (article_id, tag_id)
                VALUES (?, ?)
                """,
                (articleId, tagRow["id"]),
            )

        connection.commit()


def getArticleTags(articleId: int) -> list[str]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT article_tags.name
            FROM article_tag_relations
            JOIN article_tags ON article_tags.id = article_tag_relations.tag_id
            WHERE article_tag_relations.article_id = ?
            ORDER BY article_tags.name ASC
            """,
            (articleId,),
        ).fetchall()

    return [row["name"] for row in rows]
