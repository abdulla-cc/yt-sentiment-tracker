import sqlite3
import os

DB_FOLDER = "data"
DB_PATH = os.path.join(DB_FOLDER, "comments.db")


def init_db():
    """Create the data folder and comments table if they don't exist."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            comment_id      TEXT PRIMARY KEY,
            video_id        TEXT,
            tool            TEXT,
            author          TEXT,
            text            TEXT,
            like_count      INTEGER,
            published_at    TEXT,
            collected_at    TEXT,
            language        TEXT,
            sentiment       TEXT,
            sentiment_score REAL
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database ready at: {DB_PATH}")


def save_comment(comment):
    """Insert one comment. Ignores it silently if comment_id already exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO comments
        (comment_id, video_id, tool, author, text, like_count, published_at, collected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        comment["comment_id"],
        comment["video_id"],
        comment["tool"],
        comment["author"],
        comment["text"],
        comment["like_count"],
        comment["published_at"],
        comment["collected_at"],
    ))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
