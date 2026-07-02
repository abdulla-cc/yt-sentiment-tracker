import sqlite3
from langdetect import detect, LangDetectException

conn = sqlite3.connect("data/comments.db")
cursor = conn.cursor()

# Add the column if it doesn't exist yet
try:
    cursor.execute("ALTER TABLE comments ADD COLUMN language TEXT")
    print("Added 'language' column")
except sqlite3.OperationalError:
    print("'language' column already exists")

# Only detect for rows that don't have a language yet
cursor.execute("SELECT comment_id, text FROM comments WHERE language IS NULL")
rows = cursor.fetchall()
print(f"Detecting language for {len(rows)} comments...")

for i, (comment_id, text) in enumerate(rows, start=1):
    try:
        lang = detect(text)
    except LangDetectException:
        lang = "unknown"  # happens on empty or very short/ambiguous text

    cursor.execute(
        "UPDATE comments SET language = ? WHERE comment_id = ?",
        (lang, comment_id)
    )

    if i % 100 == 0:
        print(f"  {i}/{len(rows)} done...")
        conn.commit()

conn.commit()
conn.close()
print("Done detecting languages.")
