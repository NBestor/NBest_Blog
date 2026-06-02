from sqlite3 import IntegrityError

from app.db.database import getDatabaseConnection
from app.services.user_service import formatUser, getUserById


def _formatRelationUser(row) -> dict[str, str | int | bool | None]:
    return {
        **formatUser(row),
        "is_following": bool(row["is_following"]),
        "is_friend": bool(row["is_following"] and row["is_followed_by"]),
    }


def followUser(userId: int, followUserId: int) -> bool:
    if userId == followUserId or getUserById(followUserId) is None:
        return False

    with getDatabaseConnection() as connection:
        try:
            connection.execute(
                """
                INSERT OR IGNORE INTO follows (user_id, follow_user_id)
                VALUES (?, ?)
                """,
                (userId, followUserId),
            )
            connection.commit()
        except IntegrityError:
            return False

    return True


def unfollowUser(userId: int, followUserId: int) -> bool:
    if userId == followUserId:
        return False

    with getDatabaseConnection() as connection:
        connection.execute(
            """
            DELETE FROM follows
            WHERE user_id = ? AND follow_user_id = ?
            """,
            (userId, followUserId),
        )
        connection.commit()

    return True


def listFollowing(userId: int) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT
                users.*,
                1 AS is_following,
                CASE WHEN reverse_follow.id IS NULL THEN 0 ELSE 1 END AS is_followed_by
            FROM follows
            JOIN users ON users.id = follows.follow_user_id
            LEFT JOIN follows AS reverse_follow
                ON reverse_follow.user_id = users.id
                AND reverse_follow.follow_user_id = ?
            WHERE follows.user_id = ?
            ORDER BY follows.create_time DESC
            """,
            (userId, userId),
        ).fetchall()

    return [_formatRelationUser(row) for row in rows]


def listFollowers(userId: int) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT
                users.*,
                CASE WHEN current_follow.id IS NULL THEN 0 ELSE 1 END AS is_following,
                1 AS is_followed_by
            FROM follows
            JOIN users ON users.id = follows.user_id
            LEFT JOIN follows AS current_follow
                ON current_follow.user_id = ?
                AND current_follow.follow_user_id = users.id
            WHERE follows.follow_user_id = ?
            ORDER BY follows.create_time DESC
            """,
            (userId, userId),
        ).fetchall()

    return [_formatRelationUser(row) for row in rows]


def listFriends(userId: int) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT
                users.*,
                1 AS is_following,
                1 AS is_followed_by
            FROM follows AS current_follow
            JOIN follows AS reverse_follow
                ON reverse_follow.user_id = current_follow.follow_user_id
                AND reverse_follow.follow_user_id = current_follow.user_id
            JOIN users ON users.id = current_follow.follow_user_id
            WHERE current_follow.user_id = ?
            ORDER BY current_follow.create_time DESC
            """,
            (userId,),
        ).fetchall()

    return [_formatRelationUser(row) for row in rows]
