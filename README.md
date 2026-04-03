# News Credibility Checker

News Credibility Checker is a multi-part project for analyzing whether a news article is trustworthy. The backend is built with FastAPI and combines fake news detection, clickbait detection, News API verification, stance verification, and a final credibility score.

## Features

- Fake news detection using an ML model
- Clickbait detection
- News API based verification
- Stance verification against fetched articles
- Final credibility scoring

## Project Structure

```text
news-credibility-checker/
|-- backend/
|   |-- main.py
|   |-- requirements.txt
|   |-- pipeline/
|   |-- models/
|   |-- utils/
|-- frontend/
|-- extension/
|-- ml/
|-- docs/
```

## Backend Setup

1. Open a terminal in the `backend` folder.
2. Create and activate a virtual environment.
3. Install dependencies from `requirements.txt`.
4. Start the FastAPI server with Uvicorn.

Example:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

## API Endpoints

- `GET /`
- `GET /health`
- `POST /api/check`

## Notes

- The backend currently returns credibility-related scores for article analysis.
- The `frontend` and `extension` folders contain separate components of the overall system.
- The latest backend version removes sentiment analysis from the scoring pipeline.

## Suggested GitHub Repository Name

Recommended repository name: `news-credibility-checker`

Alternative options:

- `ai-news-credibility-checker`
- `fake-news-detection-system`
- `news-verification-platform`

## Push To GitHub

After creating a GitHub repository with the same name, connect and push your local project:

```powershell
git init
git add .
git commit -m "Initial project commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/news-credibility-checker.git
git push -u origin main
```
