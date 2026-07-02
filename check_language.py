import sqlite3

conn = sqlite3.connect("data/comments.db")
cursor = conn.cursor()

cursor.execute("SELECT language, COUNT(*) FROM comments GROUP BY language ORDER BY COUNT(*) DESC")
for lang, count in cursor.fetchall():
    print(f"{lang}: {count}")

conn.close()
