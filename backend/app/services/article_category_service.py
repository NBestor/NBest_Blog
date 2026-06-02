from sqlite3 import IntegrityError, Row

from app.db.database import getDatabaseConnection


def formatCategory(row: Row) -> dict[str, str | int]:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "name": row["name"],
        "sort_order": row["sort_order"],
        "create_time": row["create_time"],
    }


def createCategory(userId: int, name: str) -> dict[str, str | int] | None:
    categoryName = name.strip()
    if not categoryName:
        return None

    with getDatabaseConnection() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO article_categories (user_id, name)
                VALUES (?, ?)
                """,
                (userId, categoryName),
            )
            connection.commit()
        except IntegrityError:
            row = connection.execute(
                "SELECT * FROM article_categories WHERE user_id = ? AND name = ?",
                (userId, categoryName),
            ).fetchone()
            return formatCategory(row) if row else None

        row = connection.execute("SELECT * FROM article_categories WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return formatCategory(row)


def listCategories(userId: int) -> list[dict[str, str | int]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM article_categories
            WHERE user_id = ?
            ORDER BY sort_order ASC, create_time DESC, id DESC
            """,
            (userId,),
        ).fetchall()

    return [formatCategory(row) for row in rows]


def canUseCategory(userId: int, categoryId: int | None) -> bool:
    if categoryId is None:
        return True

    with getDatabaseConnection() as connection:
        row = connection.execute(
            "SELECT id FROM article_categories WHERE id = ? AND user_id = ?",
            (categoryId, userId),
        ).fetchone()
        return row is not None
