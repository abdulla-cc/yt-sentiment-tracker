import sqlite3
from scorer import score_text

conn = sqlite3.connect("data/comments.db")
cursor = conn.cursor()

# Only fetch comments that haven't been scored yet (sentiment is still NULL)
cursor.execute("SELECT comment_id, text FROM comments WHERE sentiment IS NULL")
rows = cursor.fetchall()

print(f"Scoring {len(rows)} comments...")

for i, (comment_id, text) in enumerate(rows, start=1):
    label, score = score_text(text)

    cursor.execute(
        "UPDATE comments SET sentiment = ?, sentiment_score = ? WHERE comment_id = ?",
        (label, score, comment_id)
    )

    if i % 50 == 0:
        print(f"  {i}/{len(rows)} scored...")
        conn.commit()  # save progress periodically

conn.commit()
conn.close()

print("Done scoring all comments.")
