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
        "docs": "http://127.0.0.1:8000/docs"
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


# -----------------------------
# Main API Endpoint
# -----------------------------
@app.post("/api/check", response_model=ArticleResponse)
async def check_article(payload: ArticleRequest):
    """
    Analyze a news article and return credibility metrics.
    """

    # 🔥 Clean input automatically (fix JSON/quotes issues)
    clean_title = clean_input_text(payload.title)
    clean_content = clean_input_text(payload.content)

    # Run analysis pipeline
    result = analyze_article(
        title=clean_title,
        content=clean_content,
        url=payload.url,
    )

    # Return structured response
    return ArticleResponse(
        url=payload.url,
        title=clean_title,
        content=clean_content,
        **result
    )
