import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)


def get_comments(video_id, tool, max_comments=200):
    """Pull up to max_comments from one video, handling pagination."""
    comments = []
    next_page_token = None
    collected_at = datetime.now(timezone.utc).isoformat()

    while len(comments) < max_comments:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            pageToken=next_page_token
        ).execute()

        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment_id": item["id"],
                "video_id": video_id,
                "tool": tool,
                "author": snippet["authorDisplayName"],
                "text": snippet["textDisplay"],
                "like_count": snippet["likeCount"],
                "published_at": snippet["publishedAt"],
                "collected_at": collected_at,
            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return comments[:max_comments]


if __name__ == "__main__":
    test = get_comments("aircAruvnKk", tool="ChatGPT", max_comments=150)
    print(f"Pulled {len(test)} comments")
