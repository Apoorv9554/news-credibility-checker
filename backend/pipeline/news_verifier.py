import os
import re
from difflib import SequenceMatcher

import requests
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def _text_similarity(text_a: str, text_b: str) -> float:
    return SequenceMatcher(None, text_a.lower().strip(), text_b.lower().strip()).ratio()


def extract_keywords(title: str) -> str:
    title = re.sub(r"[^a-zA-Z0-9 ]", "", title)
    words = title.split()

    stop_words = {
        "the", "is", "its", "for", "with", "and", "a", "an", "to", "of", "in",
        "on", "at", "by", "from", "as", "was", "were", "has", "had"
    }

    # Keep stronger query words and trim the query for better news API matches.
    filtered = [w for w in words if w.lower() not in stop_words]
    return " ".join(filtered[:6])


def verify_with_news_api(title: str):
    base_query = extract_keywords(title)

    queries = [
        base_query,
        " ".join(title.split()[:5]),
        " ".join(title.split()[:3]),
    ]

    if GNEWS_API_KEY:
        for q in queries:
            try:
                params = {
                    "q": q,
                    "lang": "en",
                    "max": 10,
                    "apikey": GNEWS_API_KEY,
                }
                res = requests.get("https://gnews.io/api/v4/search", params=params, timeout=10)
                data = res.json()
                articles = data.get("articles", [])
                count = len(articles)

                print(f"[GNEWS] Query: {q}, Articles: {count}")

                if count > 0:
                    return _score_articles(count), articles

            except Exception as e:
                print(f"[GNEWS ERROR]: {e}")
    else:
        print("[GNEWS] API key not configured; skipping GNews lookup.")

    if NEWS_API_KEY:
        for q in queries:
            try:
                params = {
                    "q": q,
                    "apiKey": NEWS_API_KEY,
                    "language": "en",
                    "sortBy": "relevancy",
                    "pageSize": 10,
                }
                res = requests.get("https://newsapi.org/v2/everything", params=params, timeout=10)
                data = res.json()
                articles = data.get("articles", [])
                count = len(articles)

                print(f"[NewsAPI] Query: {q}, Articles: {count}")

                if count > 0:
                    return _score_articles(count), articles

            except Exception as e:
                print(f"[NewsAPI ERROR]: {e}")
    else:
        print("[NewsAPI] API key not configured; skipping NewsAPI lookup.")

    return 0.3, []


def _score_articles(count: int) -> float:
    if count >= 8:
        return 1.0
    elif count >= 5:
        return 0.85
    elif count >= 3:
        return 0.75
    elif count >= 1:
        return 0.65
    else:
        return 0.3
