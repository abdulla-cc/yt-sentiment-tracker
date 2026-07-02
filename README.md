# YouTube AI Sentiment Tracker

A live, self-updating dashboard tracking public sentiment toward **ChatGPT, Gemini, and Microsoft Copilot** based on real YouTube comments — scored with a transformer-based sentiment model and refreshed automatically every week.

**🔗 Live dashboard:** [https://yt-sentiment-tracker-ea5avtzglszurpccwcnib2.streamlit.app/]

---

## The Question

> **Has public sentiment toward AI tools gotten more negative as they became mainstream?**

Instead of a vague "let's look at sentiment" exploration, this project is built around one falsifiable question, answered with real data and honest caveats.

## What It Found (so far)

- Overall sentiment across ~590 scored English comments is **mildly negative (≈ -0.18)** on a -1 to +1 scale
- **Copilot** shows the most consistently negative recent months (Apr–Jun 2026, all high-volume, all negative)
- Negative comments outnumber positive roughly **3:1** across all three tools
- Important caveat: YouTube comment sections skew negative/critical in general — this measures *YouTube commenter sentiment*, not overall public opinion

## How It Works

```
YouTube Data API v3
        │   collector.py      (paginated comment collection)
        ▼
SQLite database             (deduplicated via PRIMARY KEY + INSERT OR IGNORE)
        │   detect_language.py   (langdetect — non-English filtered out)
        │   scorer.py            (RoBERTa sentiment: cardiffnlp/twitter-roberta-base-sentiment-latest)
        ▼
Monthly aggregation         (confidence-weighted score: label direction × model confidence)
        │   aggregate.py
        ▼
Streamlit dashboard         (Plotly, reliability encoded as dot size)
        ▲
GitHub Actions              (weekly automated refresh, Mondays 00:00 UTC)
```

## Tech Stack

| Layer | Tools |
|---|---|
| Data collection | YouTube Data API v3, google-api-python-client |
| Storage | SQLite |
| NLP | HuggingFace Transformers — RoBERTa (twitter-roberta-base-sentiment-latest) |
| Language filtering | langdetect |
| Data handling | pandas |
| Dashboard | Streamlit + Plotly |
| Automation | GitHub Actions (cron schedule + repo write-back) |
| Hosting | Streamlit Community Cloud |

## Design Decisions Worth Noting

- **Transformer over rule-based sentiment.** VADER/TextBlob break on slang, sarcasm, and informal YouTube language. RoBERTa (trained on tweets) handles it far better — this single choice separates the results from most sentiment portfolios.
- **English-only scoring.** ~11% of collected comments are non-English; the English-tuned model scores them with false confidence, so they are detected and excluded from scoring (but kept in the database).
- **Confidence-weighted aggregation.** Each comment contributes `direction × model confidence` (positive = +1, negative = -1, neutral = 0), so a confident opinion counts more than an uncertain one.
- **Reliability is shown, not hidden.** Months with few comments aren't silently deleted — dot size encodes comment count, and a viewer-controlled slider filters thin months. The data layer stays complete; the presentation layer handles interpretation.
- **Idempotent pipeline.** Comment IDs are primary keys with `INSERT OR IGNORE`; scoring only touches unscored rows. The whole pipeline can re-run safely forever — which is what makes the weekly automation possible.

## Honest Limitations

- **Sparse time coverage.** Comments come from 6 videos, and comment timing follows video upload dates — some months have hundreds of comments, others have one. Low-volume months are visually de-emphasized rather than trusted.
- **Tool tagging is by video, not by comment.** A comment saying "ChatGPT is the worst" posted under a Copilot video counts toward Copilot's comment section sentiment.
- **YouTube negativity bias.** Comment sections skew critical regardless of topic; absolute sentiment levels matter less than *relative* differences between tools and *changes* over time.

## Automation

A GitHub Actions workflow (`.github/workflows/weekly_pull.yml`) runs every Monday:
1. Collects new comments from the tracked videos
2. Detects language on new rows
3. Scores new English comments with RoBERTa
4. Rebuilds the monthly aggregation
5. Commits the refreshed CSVs back to the repo — which triggers the dashboard to update

## Run It Locally

```bash
git clone https://github.com/abdulla-cc/yt-sentiment-tracker.git
cd yt-sentiment-tracker
python -m venv venv
source venv/Scripts/activate        # Windows Git Bash
pip install -r requirements.txt

# Add your YouTube Data API v3 key
echo "YOUTUBE_API_KEY=your_key_here" > .env

python run_collection.py            # collect comments
python detect_language.py           # tag languages
python reset_and_score_english.py   # sentiment scoring (English only)
python aggregate.py                 # build monthly trend
streamlit run app.py                # launch dashboard
```

## Author

**Abdalla Nadir** — Final-year B.CS (AI) student, Multimedia University
[LinkedIn](https://www.linkedin.com/in/abdalla-nadir-a6841532b/) · [GitHub](https://github.com/abdulla-cc)
