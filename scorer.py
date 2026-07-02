from transformers import pipeline

# This downloads the model the first time (a few hundred MB) then caches it locally
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)


def score_text(text):
    """Run one comment through RoBERTa. Returns (label, confidence)."""
    result = sentiment_pipeline(text[:512])[0]  # truncate to 512 chars, model's limit
    return result["label"], result["score"]


if __name__ == "__main__":
    samples = [
        "This is amazing, I love it!",
        "Worst video ever, complete waste of time.",
        "It's okay I guess, nothing special.",
    ]

    for text in samples:
        label, score = score_text(text)
        print(f"{label} ({score:.2f}) | {text}")
