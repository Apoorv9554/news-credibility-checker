import requests
from urllib.parse import urlparse

NEWS_API_KEY = "6395b3b535fc448ca824844938639b1b"


def extract_keywords(title: str) -> str:
    stop_words = {
        "the","is","its","for","with","and","a","an","to","of","in"
    }

    words = [
        word.lower()
        for word in title.split()
        if word.lower() not in stop_words
    ]

    return " ".join(words[:6])


def verify_with_news_api(title: str):
    query = extract_keywords(title)

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10,
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        articles = data.get("articles", [])
        count = len(articles)

        print(f"[news_verifier] Query: {query}, Articles found: {count}")

        if count >= 10:
            score = 1.0
        elif count >= 6:
            score = 0.9
        elif count >= 4:
            score = 0.8
        elif count >= 2:
            score = 0.7
        elif count >= 1:
            score = 0.6
        else:
            score = 0.2

        return score, articles

    except Exception as e:
        print(f"[news_verifier] Error: {e}")
        return 0.5, []
    