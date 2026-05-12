from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from pipeline.analyzer import analyze_article
from utils.text_cleaner import clean_input_text


# -----------------------------
# FastAPI App Initialization
# -----------------------------
app = FastAPI(
    title="News Credibility Checker API",
    version="1.0.0",
    description="AI-powered system to analyze and verify news credibility using ML, News API, and stance detection."
)

# -----------------------------
# Enable CORS (for frontend)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Root Endpoint (for browser)
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "News Credibility Checker API is running 🚀",
        "docs": "http://127.0.0.1:8001/docs"
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# -----------------------------
# Request Model
# -----------------------------
class ArticleRequest(BaseModel):
    url: Optional[str] = None
    title: str
    content: str


# -----------------------------
# Response Model
# -----------------------------
class ArticleResponse(BaseModel):
    url: Optional[str] = None
    title: str
    content: str

    clickbait_score: float
    fake_probability: float

    news_verification_score: float   # 🔥 Added
    stance_score: float              # 🔥 Added
    source_reputation: float

    credibility_score: float


def build_fallback_response(url: Optional[str], title: str, content: str) -> ArticleResponse:
    return ArticleResponse(
        url=url,
        title=title,
        content=content,
        clickbait_score=0.7,
        fake_probability=0.5,
        news_verification_score=0.3,
        stance_score=0.5,
        source_reputation=0.3,
        credibility_score=52.5,
    )


def run_analysis(url: Optional[str], title: str, content: str) -> ArticleResponse:
    clean_title = clean_input_text(title)
    clean_content = clean_input_text(content)

    if len(clean_title) > 500:
        clean_title = clean_title[:500].strip()

    if len(clean_content) > 12000:
        clean_content = clean_content[:12000].strip()

    if not clean_title:
        clean_title = "Untitled article"

    if not clean_content:
        clean_content = "No article content extracted."

    try:
        result = analyze_article(
            title=clean_title,
            content=clean_content,
            url=url,
        )
    except Exception as exc:
        print(f"[api] Unexpected analysis error: {exc}")
        return build_fallback_response(
            url=url,
            title=clean_title,
            content=clean_content,
        )

    return ArticleResponse(
        url=url,
        title=clean_title,
        content=clean_content,
        **result
    )


# -----------------------------
# Main API Endpoint
# -----------------------------
@app.post("/api/check", response_model=ArticleResponse)
async def check_article(payload: ArticleRequest):
    """
    Analyze a news article and return credibility metrics.
    """

    return run_analysis(
        url=payload.url,
        title=payload.title,
        content=payload.content,
    )


@app.post("/api/extension-check", response_model=ArticleResponse)
async def check_article_for_extension(payload: ArticleRequest):
    """
    Dedicated endpoint for the browser extension with extra input hardening.
    """
    return run_analysis(
        url=payload.url,
        title=payload.title,
        content=payload.content,
    )
