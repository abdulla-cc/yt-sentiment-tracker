import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="YouTube AI Sentiment Tracker", layout="wide")

st.title("YouTube AI Sentiment Tracker")
st.caption("Tracking sentiment toward ChatGPT, Gemini, and Copilot from YouTube comments")

# ---- Load data ----
df = pd.read_csv("data/monthly_sentiment.csv")
df["month"] = pd.to_datetime(df["month"])

# ---- Sidebar controls ----
tools = st.sidebar.multiselect(
    "Select tools to display",
    options=df["tool"].unique(),
    default=df["tool"].unique()
)

min_comments = st.sidebar.slider(
    "Minimum comments per month (filters out noisy months)",
    min_value=1,
    max_value=int(df["comment_count"].max()),
    value=5
)

filtered = df[(df["tool"].isin(tools)) & (df["comment_count"] >= min_comments)]

# ---- KPI cards ----
overall_avg = filtered["avg_sentiment"].mean()
total_comments = filtered["comment_count"].sum()

if not filtered.empty:
    by_tool_avg = filtered.groupby("tool")["avg_sentiment"].mean()
    most_positive_tool = by_tool_avg.idxmax()
    most_negative_tool = by_tool_avg.idxmin()
else:
    most_positive_tool = most_negative_tool = "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Comments analyzed", f"{total_comments:,}")
col2.metric("Overall sentiment", f"{overall_avg:.2f}" if not filtered.empty else "N/A")
col3.metric("Most positive tool", most_positive_tool)
col4.metric("Most negative tool", most_negative_tool)

# ---- Insight text ----
st.markdown(
    f"**Reading the chart:** dot size shows how many comments back each point — "
    f"bigger dots are more trustworthy. At the current filter (≥{min_comments} comments/month), "
    f"**{most_negative_tool}** trends most negative and **{most_positive_tool}** trends most positive."
)

# ---- Chart ----
fig = px.scatter(
    filtered,
    x="month",
    y="avg_sentiment",
    color="tool",
    size="comment_count",
    size_max=40,
    hover_data=["comment_count"],
    title="Monthly Sentiment by Tool (dot size = number of comments)"
)
fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.update_layout(yaxis_title="Sentiment (-1 = negative, +1 = positive)")
st.plotly_chart(fig, use_container_width=True)

# ---- Sample comments ----
st.subheader("Sample comments")

comments_df = pd.read_csv("data/scored_comments.csv")

for tool in tools:
    tool_comments = comments_df[comments_df["tool"] == tool]
    if tool_comments.empty:
        continue

    st.markdown(f"**{tool}**")
    c1, c2 = st.columns(2)

    top_positive = tool_comments[tool_comments["sentiment"] == "positive"] \
        .sort_values("sentiment_score", ascending=False).head(2)
    top_negative = tool_comments[tool_comments["sentiment"] == "negative"] \
        .sort_values("sentiment_score", ascending=False).head(2)

    with c1:
        st.markdown("*Most positive*")
        for _, row in top_positive.iterrows():
            st.success(row["text"][:150])

    with c2:
        st.markdown("*Most negative*")
        for _, row in top_negative.iterrows():
            st.error(row["text"][:150])

# ---- Raw data ----
st.subheader("Raw monthly data")
st.dataframe(filtered.sort_values("month"))