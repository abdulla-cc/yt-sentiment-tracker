import sqlite3
import pandas as pd

conn = sqlite3.connect("data/comments.db")

df = pd.read_sql_query("""
    SELECT tool, published_at, sentiment, sentiment_score
    FROM comments
    WHERE sentiment IS NOT NULL
""", conn)
conn.close()

df["published_at"] = pd.to_datetime(df["published_at"])

direction = {"positive": 1, "negative": -1, "neutral": 0}
df["direction"] = df["sentiment"].map(direction)
df["weighted_score"] = df["direction"] * df["sentiment_score"]

# Assign each comment to its calendar month instead of week
df["month"] = df["published_at"].dt.to_period("M").dt.to_timestamp()

# Group by month + tool — average sentiment AND count of comments per bucket
monthly = (
    df.groupby(["month", "tool"])["weighted_score"]
    .agg(avg_sentiment="mean", comment_count="count")
    .reset_index()
)

monthly = monthly.sort_values(["month", "tool"])

print(monthly.to_string(index=False))

monthly.to_csv("data/monthly_sentiment.csv", index=False)
print("\nSaved to data/monthly_sentiment.csv")
