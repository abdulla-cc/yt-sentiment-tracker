from collector import get_comments
from database import init_db, save_comment

init_db()

VIDEOS = [
    {"id": "MmFLDvOFLW0", "tool": "ChatGPT"},
    {"id": "gHkKPvWj43g", "tool": "ChatGPT"},
    {"id": "75xzAc7WyOw", "tool": "Gemini"},
    {"id": "UH2_Sgeu4lc", "tool": "Gemini"},
    {"id": "WAQbtOFZ4ig", "tool": "Copilot"},
    {"id": "5-tzLvOu9lo", "tool": "Copilot"},
]

total_saved = 0

for video in VIDEOS:
    print(f"Collecting from {video['tool']} video {video['id']}...")
    comments = get_comments(video["id"], tool=video["tool"], max_comments=200)

    for c in comments:
        save_comment(c)

    total_saved += len(comments)
    print(f"  -> pulled {len(comments)} comments")

print(f"\nDone. Processed {total_saved} comments across {len(VIDEOS)} video(s).")
