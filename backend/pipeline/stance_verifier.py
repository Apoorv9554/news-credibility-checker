import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(text1: str, text2: str) -> float:
    """
    Returns cosine similarity between two texts (0 to 1)
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([text1, text2])
    sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return float(sim)


def compute_stance_score(input_text: str, articles: list) -> float:
    """
    Compute agreement score based on similarity with related articles.
    articles = list of dicts from News API
    """

    if not articles:
        return 0.5  # neutral if no evidence

    scores = []

    for art in articles:
        title = art.get("title", "")
        desc = art.get("description", "")

        content = art.get("content", "")
        combined = f"{title} {desc} {content}".strip()

        if combined:
            sim = compute_similarity(input_text, combined)
            scores.append(sim)

    if not scores:
        return 0.5

    avg_score = np.mean(scores)

# Boost similarity (VERY IMPORTANT)
    avg_score = min(1.0, avg_score * 5)

    print(f"[stance] boosted similarity: {avg_score}")

    if avg_score >= 0.4:
        return 1.0
    elif avg_score >= 0.2:
        return 0.8
    else:
        return 0.5
    
