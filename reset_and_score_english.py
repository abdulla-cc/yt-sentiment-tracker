import sqlite3
from scorer import score_text

conn = sqlite3.connect("data/comments.db")
cursor = conn.cursor()

# Clear sentiment on anything that isn't English — undoes the earlier noisy scoring
cursor.execute("""
    UPDATE comments
    SET sentiment = NULL, sentiment_score = NULL
    WHERE language != 'en'
""")
print(f"Cleared sentiment on {cursor.rowcount} non-English comments")
conn.commit()

# Score only English comments that don't have sentiment yet
cursor.execute("""
    SELECT comment_id, text FROM comments
    WHERE language = 'en' AND sentiment IS NULL
""")
rows = cursor.fetchall()
print(f"Scoring {len(rows)} English comments...")

for i, (comment_id, text) in enumerate(rows, start=1):
    label, score = score_text(text)
    cursor.execute(
        "UPDATE comments SET sentiment = ?, sentiment_score = ? WHERE comment_id = ?",
        (label, score, comment_id)
    )
    if i % 50 == 0:
        print(f"  {i}/{len(rows)} scored...")
        conn.commit()

conn.commit()
conn.close()
print("Done. Only English comments now have sentiment scores.")
