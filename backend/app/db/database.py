import sqlite3
from pathlib import Path

from app.core.config import getSettings
from app.core.security import getPasswordHash


def getDatabasePath() -> Path:
    databaseUrl = getSettings().database_url
    return Path(databaseUrl.replace("sqlite:///", ""))


def getDatabaseConnection() -> sqlite3.Connection:
    databasePath = getDatabasePath()
    databasePath.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(databasePath)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initDatabase() -> None:
    with getDatabaseConnection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS app_metadata (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                app_name TEXT NOT NULL,
                initialized_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO app_metadata (id, app_name)
            VALUES (1, ?)
            """,
            (getSettings().app_name,),
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                nickname TEXT NOT NULL,
                avatar_url TEXT,
                signature TEXT,
                role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)")
        supervisorRow = connection.execute("SELECT * FROM users WHERE id = 0").fetchone()
        if supervisorRow is None:
            connection.execute(
                """
                INSERT INTO users (id, username, password_hash, nickname, role)
                VALUES (?, ?, ?, ?, ?)
                """,
                (0, "NBest", getPasswordHash("NBest666"), "NBest", "admin"),
            )
        else:
            connection.execute(
                """
                UPDATE users
                SET username = ?, nickname = ?, role = ?
                WHERE id = 0
                """,
                ("NBest", "NBest", "admin"),
            )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                follow_user_id INTEGER NOT NULL,
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, follow_user_id),
                CHECK(user_id != follow_user_id),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(follow_user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_follows_user_id ON follows (user_id)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_follows_follow_user_id ON follows (follow_user_id)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                summary TEXT,
                content TEXT NOT NULL,
                is_draft INTEGER NOT NULL DEFAULT 1 CHECK(is_draft IN (0, 1)),
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        articleColumns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(articles)").fetchall()
        }
        if "category_id" not in articleColumns:
            connection.execute("ALTER TABLE articles ADD COLUMN category_id INTEGER")
        if "visible_type" not in articleColumns:
            connection.execute("ALTER TABLE articles ADD COLUMN visible_type TEXT NOT NULL DEFAULT 'self'")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_articles_user_draft ON articles (user_id, is_draft)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS article_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                sort_order INTEGER NOT NULL DEFAULT 0,
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, name),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_article_categories_user_id ON article_categories (user_id)"
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS article_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, name),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_article_tags_user_id ON article_tags (user_id)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS article_tag_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                UNIQUE(article_id, tag_id),
                FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE,
                FOREIGN KEY(tag_id) REFERENCES article_tags(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_article_tag_relations_article_id ON article_tag_relations (article_id)"
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                source_type TEXT NOT NULL,
                visible_type TEXT NOT NULL DEFAULT 'self',
                upload_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_photos_user_id ON photos (user_id)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_photos_visible_type ON photos (visible_type)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                article_id INTEGER NOT NULL,
                parent_id INTEGER,
                content TEXT NOT NULL,
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE,
                FOREIGN KEY(parent_id) REFERENCES comments(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_comments_article_id ON comments (article_id)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS like_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                target_type TEXT NOT NULL,
                target_id INTEGER NOT NULL,
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, target_type, target_id),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_like_records_target ON like_records (target_type, target_id)"
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS collects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                article_id INTEGER NOT NULL,
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, article_id),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_collects_article_id ON collects (article_id)")
        userColumns = {row["name"] for row in connection.execute("PRAGMA table_info(users)").fetchall()}
        if "quick_post_default_visible_type" not in userColumns:
            connection.execute(
                "ALTER TABLE users ADD COLUMN quick_post_default_visible_type TEXT NOT NULL DEFAULT 'public'"
            )
        commentColumns = {row["name"] for row in connection.execute("PRAGMA table_info(comments)").fetchall()}
        if "target_type" not in commentColumns:
            connection.execute("ALTER TABLE comments ADD COLUMN target_type TEXT NOT NULL DEFAULT 'article'")
        if "target_id" not in commentColumns:
            connection.execute("ALTER TABLE comments ADD COLUMN target_id INTEGER")
            connection.execute("UPDATE comments SET target_id = article_id WHERE target_id IS NULL")
        if "parent_id" not in commentColumns:
            connection.execute("ALTER TABLE comments ADD COLUMN parent_id INTEGER")
        commentColumnInfo = {
            row["name"]: row
            for row in connection.execute("PRAGMA table_info(comments)").fetchall()
        }
        if commentColumnInfo["article_id"]["notnull"]:
            connection.execute("DROP INDEX IF EXISTS idx_comments_article_id")
            connection.execute("DROP INDEX IF EXISTS idx_comments_target")
            connection.execute("ALTER TABLE comments RENAME TO comments_old")
            connection.execute(
                """
                CREATE TABLE comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    article_id INTEGER,
                    parent_id INTEGER,
                    target_type TEXT NOT NULL DEFAULT 'article',
                    target_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE,
                    FOREIGN KEY(parent_id) REFERENCES comments(id) ON DELETE CASCADE
                )
                """
            )
            connection.execute(
                """
                INSERT INTO comments (
                    id,
                    user_id,
                    article_id,
                    parent_id,
                    target_type,
                    target_id,
                    content,
                    create_time
                )
                SELECT
                    id,
                    user_id,
                    article_id,
                    parent_id,
                    COALESCE(target_type, 'article'),
                    COALESCE(target_id, article_id),
                    content,
                    create_time
                FROM comments_old
                """
            )
            connection.execute("DROP TABLE comments_old")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_comments_target ON comments (target_type, target_id)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_comments_parent_id ON comments (parent_id)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS quick_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                visible_type TEXT NOT NULL DEFAULT 'public',
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_quick_posts_user_id ON quick_posts (user_id)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS quick_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_quick_notes_user_id ON quick_notes (user_id)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT,
                due_date TEXT,
                is_done INTEGER NOT NULL DEFAULT 0 CHECK(is_done IN (0, 1)),
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_todos_user_id ON todos (user_id)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_todos_user_done ON todos (user_id, is_done)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_todos_user_due_date ON todos (user_id, due_date)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS calendar_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_type TEXT NOT NULL DEFAULT 'other' CHECK(event_type IN ('birthday', 'anniversary', 'other')),
                note TEXT,
                is_yearly INTEGER NOT NULL DEFAULT 0 CHECK(is_yearly IN (0, 1)),
                create_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                update_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_calendar_events_user_id ON calendar_events (user_id)")
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_calendar_events_user_date ON calendar_events (user_id, event_date)"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_calendar_events_user_yearly ON calendar_events (user_id, is_yearly)"
        )
        connection.commit()

        # Ensure Niubao AI bot account exists (ID=666)
        niubaoRow = connection.execute("SELECT * FROM users WHERE id = 666").fetchone()
        if niubaoRow is None:
            connection.execute(
                """
                INSERT INTO users (id, username, password_hash, nickname, role)
                VALUES (?, ?, ?, ?, ?)
                """,
                (666, "niubao", getPasswordHash("niubao_bot_666_internal"), "牛宝", "user"),
            )
        else:
            connection.execute(
                "UPDATE users SET username = ?, nickname = ?, role = ? WHERE id = 666",
                ("niubao", "牛宝", "user"),
            )
        connection.commit()

        # Ensure Niubao is friends with all existing users
        existingUsers = connection.execute(
            "SELECT id FROM users WHERE id != 666"
        ).fetchall()
        for userRow in existingUsers:
            connection.execute(
                "INSERT OR IGNORE INTO follows (user_id, follow_user_id) VALUES (?, ?)",
                (666, userRow["id"]),
            )
            connection.execute(
                "INSERT OR IGNORE INTO follows (user_id, follow_user_id) VALUES (?, ?)",
                (userRow["id"], 666),
            )
        connection.commit()


def canConnectDatabase() -> bool:
    with getDatabaseConnection() as connection:
        row = connection.execute("SELECT 1 AS is_connected").fetchone()
        return bool(row and row["is_connected"] == 1)
