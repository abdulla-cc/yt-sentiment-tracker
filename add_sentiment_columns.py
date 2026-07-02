import sqlite3

conn = sqlite3.connect("data/comments.db")
cursor = conn.cursor()

# ALTER TABLE adds a new column to an existing table
try:
    cursor.execute("ALTER TABLE comments ADD COLUMN sentiment TEXT")
    print("Added 'sentiment' column")
except sqlite3.OperationalError:
    print("'sentiment' column already exists")

try:
    cursor.execute("ALTER TABLE comments ADD COLUMN sentiment_score REAL")
    print("Added 'sentiment_score' column")
except sqlite3.OperationalError:
    print("'sentiment_score' column already exists")

conn.commit()
conn.close()
