import sqlite3

conn = sqlite3.connect("data/comments.db")
cursor = conn.cursor()

print("Overall sentiment breakdown:")
cursor.execute("SELECT sentiment, COUNT(*) FROM comments GROUP BY sentiment")
for sentiment, count in cursor.fetchall():
    print(f"  {sentiment}: {count}")

print("\nSentiment breakdown by tool (English only):")
cursor.execute("""
    SELECT tool, sentiment, COUNT(*)
    FROM comments
    WHERE sentiment IS NOT NULL
    GROUP BY tool, sentiment
    ORDER BY tool, sentiment
""")
for tool, sentiment, count in cursor.fetchall():
    print(f"  {tool} - {sentiment}: {count}")

print("\nSample scored comments:")
cursor.execute("""
    SELECT tool, sentiment, sentiment_score, text
    FROM comments
    WHERE sentiment IS NOT NULL
    LIMIT 5
""")
for tool, sentiment, score, text in cursor.fetchall():
    print(f"  [{tool}] {sentiment} ({score:.2f}) | {text[:60]}")

conn.close()
