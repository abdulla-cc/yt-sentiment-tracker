import sqlite3

conn = sqlite3.connect("data/comments.db")
cursor = conn.cursor()

# Count total rows
cursor.execute("SELECT COUNT(*) FROM comments")
total = cursor.fetchone()[0]
print(f"Total comments in database: {total}\n")

# Show first 5 rows
cursor.execute("SELECT author, tool, published_at, text FROM comments LIMIT 5")
for row in cursor.fetchall():
    author, tool, date, text = row
    print(f"[{tool}] {author} ({date[:10]})")
    print(f"   {text[:60]}")
    print()

conn.close()
