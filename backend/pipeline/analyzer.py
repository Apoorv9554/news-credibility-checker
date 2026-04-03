from typing import Optional
from .news_verifier import verify_with_news_api
from .fake_news_model import predict_fake_probability
from .clickbait_model import predict_clickbait_score
from .stance_verifier import compute_stance_score


def analyze_article(
    title: str,
    content: str,
    url: Optional[str] = None,
) -> dict:

    # 1) Fake-news probability
    text_for_fake_model = f"{title} {content}"
    fake_probability = predict_fake_probability(text_for_fake_model)

    # 2) Clickbait score
    clickbait_score = predict_clickbait_score(title)

    # 3) News API verification
    try:
        news_verification_score, articles = verify_with_news_api(title)
    except Exception as e:
        print(f"[analyzer] News API error: {e}")
        news_verification_score, articles = 0.5, []

    print(f"[analyzer] Articles fetched: {len(articles)}")

    # 4) Stance verification
    try:
        stance_score = compute_stance_score(title + " " + content, articles)
    except Exception as e:
        print(f"[analyzer] Stance error: {e}")
        stance_score = 0.5

    print(f"[analyzer] Stance score: {stance_score}")

    # -----------------------------
    # 5) Improved Credibility Calculation
    # -----------------------------

    # Stabilize fake model impact (prevents real news from being penalized too much)
    fake_component = max(0.5, 1 - fake_probability)

    # New weighted scoring (prioritize real-world evidence + agreement)
    credibility = (
        0.25 * fake_component +
        0.40 * news_verification_score +
        0.30 * stance_score +
        0.05 * clickbait_score
    ) * 100

    # Bonus for strong agreement (boost only true news)
    if news_verification_score >= 0.8 and stance_score >= 0.7:
        credibility += 5

    # Cap at 100
    credibility = min(100, credibility)

    # -----------------------------
    # Response
    # -----------------------------
    return {
        "clickbait_score": float(clickbait_score),
        "fake_probability": float(fake_probability),
        "news_verification_score": float(news_verification_score),
        "stance_score": float(stance_score),
        "source_reputation": float(news_verification_score),
        "credibility_score": float(round(credibility, 2)),
    }