from datetime import date, timedelta
from sqlite3 import Row

from app.db.database import getDatabaseConnection


def formatTodo(row: Row) -> dict[str, str | int | bool | None]:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "title": row["title"],
        "content": row["content"],
        "category": row["category"],
        "due_date": row["due_date"],
        "is_done": bool(row["is_done"]),
        "create_time": row["create_time"],
        "update_time": row["update_time"],
    }


def listTodos(userId: int) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM todos
            WHERE user_id = ?
            ORDER BY is_done ASC, due_date IS NULL ASC, due_date ASC, update_time DESC, id DESC
            """,
            (userId,),
        ).fetchall()

    return [formatTodo(row) for row in rows]


def createTodo(
    userId: int,
    title: str,
    content: str | None,
    category: str | None,
    dueDate: str | None,
) -> dict[str, str | int | bool | None]:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO todos (user_id, title, content, category, due_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (userId, title, content, category, dueDate),
        )
        connection.commit()
        row = connection.execute("SELECT * FROM todos WHERE id = ?", (cursor.lastrowid,)).fetchone()

    return formatTodo(row)


def updateTodo(
    userId: int,
    todoId: int,
    title: str,
    content: str | None,
    category: str | None,
    dueDate: str | None,
    isDone: bool,
) -> dict[str, str | int | bool | None] | None:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            """
            UPDATE todos
            SET title = ?,
                content = ?,
                category = ?,
                due_date = ?,
                is_done = ?,
                update_time = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (title, content, category, dueDate, int(isDone), todoId, userId),
        )
        if cursor.rowcount == 0:
            return None
        connection.commit()
        row = connection.execute("SELECT * FROM todos WHERE id = ? AND user_id = ?", (todoId, userId)).fetchone()

    return formatTodo(row)


def setTodoDone(userId: int, todoId: int, isDone: bool) -> dict[str, str | int | bool | None] | None:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            """
            UPDATE todos
            SET is_done = ?, update_time = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (int(isDone), todoId, userId),
        )
        if cursor.rowcount == 0:
            return None
        connection.commit()
        row = connection.execute("SELECT * FROM todos WHERE id = ? AND user_id = ?", (todoId, userId)).fetchone()

    return formatTodo(row)


def deleteTodo(userId: int, todoId: int) -> bool:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            "DELETE FROM todos WHERE id = ? AND user_id = ?",
            (todoId, userId),
        )
        connection.commit()
        return cursor.rowcount > 0


def listTodoReminders(userId: int) -> list[dict[str, str | int | bool | None]]:
    today = date.today()
    remindUntil = today + timedelta(days=1)
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM todos
            WHERE user_id = ?
              AND is_done = 0
              AND due_date IS NOT NULL
              AND due_date <= ?
            ORDER BY due_date ASC, id ASC
            """,
            (userId, remindUntil.isoformat()),
        ).fetchall()

    return [formatTodo(row) for row in rows]
