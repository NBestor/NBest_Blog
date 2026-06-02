from sqlite3 import Row

from app.db.database import getDatabaseConnection


def formatQuickNote(row: Row) -> dict[str, str | int]:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "content": row["content"],
        "create_time": row["create_time"],
        "update_time": row["update_time"],
    }


def listQuickNotes(userId: int) -> list[dict[str, str | int]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM quick_notes
            WHERE user_id = ?
            ORDER BY update_time DESC, id DESC
            """,
            (userId,),
        ).fetchall()

    return [formatQuickNote(row) for row in rows]


def searchQuickNotes(userId: int, query: str) -> list[dict[str, str | int]]:
    normalizedQuery = query.strip().lower()
    if not normalizedQuery:
        return []

    return [
        note
        for note in listQuickNotes(userId)
        if normalizedQuery in str(note["content"]).lower()
    ]


def createQuickNote(userId: int, content: str) -> dict[str, str | int]:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            "INSERT INTO quick_notes (user_id, content) VALUES (?, ?)",
            (userId, content),
        )
        connection.commit()
        row = connection.execute("SELECT * FROM quick_notes WHERE id = ?", (cursor.lastrowid,)).fetchone()

    return formatQuickNote(row)


def deleteQuickNote(userId: int, quickNoteId: int) -> bool:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            "DELETE FROM quick_notes WHERE id = ? AND user_id = ?",
            (quickNoteId, userId),
        )
        connection.commit()
        return cursor.rowcount > 0
