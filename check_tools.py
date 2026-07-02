import sqlite3

conn = sqlite3.connect("data/comments.db")
cursor = conn.cursor()

cursor.execute("SELECT tool, COUNT(*) FROM comments GROUP BY tool")
for tool, count in cursor.fetchall():
    print(f"{tool}: {count} comments")

conn.close()
