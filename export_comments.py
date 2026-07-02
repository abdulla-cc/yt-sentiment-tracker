import sqlite3
import pandas as pd

conn = sqlite3.connect("data/comments.db")
query = "SELECT tool, sentiment, sentiment_score, text FROM comments WHERE sentiment IS NOT NULL"
df = pd.read_sql_query(query, conn)
conn.close()

df.to_csv("data/scored_comments.csv", index=False)
print(f"Exported {len(df)} scored comments to data/scored_comments.csv")
