
# 🛡️ AI-Powered News Credibility Checker
### Hybrid Fake News Detection using Machine Learning, NLP, API Verification & Stance Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Ensemble-orange)
![NLP](https://img.shields.io/badge/NLP-TF--IDF-yellow)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-success?logo=googlechrome)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-purple)

</div>

---

# 📖 Table of Contents

- [Introduction](#-introduction)
- [Problem Statement](#-problem-statement)
- [Project Objectives](#-project-objectives)
- [Core Features](#-core-features)
- [System Architecture](#-system-architecture)
- [Project Workflow](#-project-workflow)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation Guide](#-installation-guide)
- [Environment Configuration](#-environment-configuration)
- [Running the Backend](#-running-the-backend)
- [Frontend Setup](#-frontend-setup)
- [Chrome Extension Setup](#-chrome-extension-setup)
- [API Documentation](#-api-documentation)
- [Model Training](#-model-training)
- [Scoring Methodology](#-scoring-methodology)
- [Research & Technical Contributions](#-research--technical-contributions)
- [Future Improvements](#-future-improvements)
- [Security Notes](#-security-notes)
- [Authors](#-authors)

---

# 🌍 Introduction

The rapid growth of online news platforms and social media has significantly increased the spread of fake news, misinformation, and manipulated content. Traditional fact-checking methods are often slow, manual, and unable to process the enormous amount of information generated every second.

The **AI-Powered News Credibility Checker** is a hybrid misinformation detection platform designed to analyze news articles and determine their credibility using:

- Machine Learning
- Natural Language Processing (NLP)
- Real-Time News Verification APIs
- Stance Verification
- Weighted Multi-Module Scoring

Unlike traditional fake news detection systems that rely solely on dataset-based classification, this project combines internal machine learning prediction with real-world external verification mechanisms.

---

# ❗ Problem Statement

Modern fake news articles are designed to imitate authentic journalism. They often:

- Use sensational clickbait headlines
- Manipulate emotional language
- Spread rapidly on social media
- Mislead public opinion

Traditional ML models may achieve high accuracy on datasets but fail in real-world scenarios because:

- News patterns constantly evolve
- Datasets are biased
- Real-world context changes dynamically

This project addresses these limitations using a hybrid architecture.

---

# 🎯 Project Objectives

The primary objectives of this project are:

- Detect fake or misleading news articles
- Analyze clickbait headlines
- Verify news using trusted external APIs
- Compare stance between input article and real-world sources
- Generate a final credibility score
- Provide real-time analysis using FastAPI
- Support browser extension integration

---

# ✨ Core Features

---

## 🤖 1. Fake News Detection

Uses a Soft Voting Ensemble consisting of:

- Logistic Regression
- Random Forest
- SGD Classifier

to classify whether a news article is fake or real.

---

## 📰 2. Clickbait Detection

Analyzes only the article headline to determine whether it contains sensational or misleading patterns.

---

## 🌐 3. Live News Verification

Fetches related news articles using:

- GNews API
- NewsAPI

to verify whether the submitted news exists in trusted news ecosystems.

---

## 🧠 4. Stance Verification

Uses TF-IDF vectorization and cosine similarity to determine whether retrieved external articles support or contradict the user’s article.

---

## 📊 5. Final Credibility Score

Combines:

- Fake Probability
- Clickbait Analysis
- News Verification
- Stance Agreement

into a single credibility score.

---

# 🧠 System Architecture

```text
┌──────────────────────┐
│      User Input      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Text Preprocessing  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ TF-IDF Vectorization │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Ensemble ML Model    │
│ (Fake Probability)   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Clickbait Detection  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ API Verification     │
│ (GNews + NewsAPI)    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Stance Verification  │
│ (Cosine Similarity)  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Score Aggregation    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Final Credibility    │
│ Score Output         │
└──────────────────────┘
````

---

# 🔄 Project Workflow

1. User submits title + content
2. Text preprocessing begins
3. TF-IDF converts text into vectors
4. Ensemble model predicts fake probability
5. Headline analyzed for clickbait
6. APIs fetch external related articles
7. Stance similarity is computed
8. Weighted scoring formula calculates credibility
9. Results displayed to user

---

# 🤖 Machine Learning Pipeline

## 🔹 Data Preprocessing

The following preprocessing steps are performed:

* Lowercasing
* URL removal
* HTML stripping
* Regex cleaning
* Whitespace normalization

```python
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
```

---

## 🔹 TF-IDF Vectorization

```python
TfidfVectorizer(
    max_features=30000,
    ngram_range=(1,2),
    stop_words="english",
    min_df=2,
    max_df=0.9,
    sublinear_tf=True
)
```

---

## 🔹 Ensemble Learning

```python
VotingClassifier(
    estimators=[
        ("lr", lr_model),
        ("rf", rf_model),
        ("sgd", sgd_model)
    ],
    voting="soft"
)
```

---

# 🌐 Live API Verification

The project integrates:

* GNews API
* NewsAPI

to validate whether similar articles exist online.

### Query Strategy

* Initial keyword extraction
* Dynamic fallback shortening
* Multi-query retry mechanism

---

# 🧠 Stance Verification

The system computes similarity between:

* User article
* External verified articles

using:

* TF-IDF
* Cosine Similarity

```python
cosine_similarity(vectors[0:1], vectors[1:2])
```

---

# 📊 Scoring Methodology

Final credibility score:

```text
Credibility Score =
  0.25 × Fake Model +
  0.05 × Clickbait +
  0.40 × API Verification +
  0.30 × Stance Verification
```

---

# 🛠️ Technology Stack

## Backend

* FastAPI
* Python
* Uvicorn

## Machine Learning

* Scikit-learn
* TF-IDF
* Ensemble Learning

## NLP

* Text preprocessing
* Cosine Similarity

## APIs

* GNews API
* NewsAPI

## Frontend

* HTML
* CSS
* JavaScript

## Browser Extension

* Chrome Manifest V3

---

# 🗂️ Project Structure

```text
news-credibility-checker/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   ├── pipeline/
│   │   ├── analyzer.py
│   │   ├── fake_news_model.py
│   │   ├── clickbait_model.py
│   │   ├── news_verifier.py
│   │   └── stance_verifier.py
│   │
│   └── utils/
│
├── frontend/
│
├── extension/
│
├── ml/
│   ├── train_fake_news_model.py
│   └── datasets/
│
├── docs/
│
└── README.md
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/news-credibility-checker.git
cd news-credibility-checker
```

---

## 2️⃣ Create Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

# 🔑 Environment Configuration

Create `.env` file:

```env
GNEWS_API_KEY=your_gnews_key
NEWS_API_KEY=your_newsapi_key
```

---

# 🚀 Running the Backend

```bash
cd backend
uvicorn main:app --reload
```

---

# 🌐 API Access

| Service      | URL                                                      |
| ------------ | -------------------------------------------------------- |
| Backend      | [http://127.0.0.1:8000](http://127.0.0.1:8000)           |
| Swagger Docs | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |

---

# 📡 API Endpoints

| Method | Endpoint     | Description     |
| ------ | ------------ | --------------- |
| GET    | `/`          | API status      |
| GET    | `/health`    | Health check    |
| POST   | `/api/check` | Analyze article |

---

# 📥 Example Request

```json
{
  "title": "NASA launches Artemis mission",
  "content": "NASA announced a new moon mission...",
  "url": "https://example.com"
}
```

---

# 📤 Example Response

```json
{
  "fake_probability": 0.14,
  "clickbait_score": 0.91,
  "news_verification_score": 0.85,
  "stance_score": 1.0,
  "credibility_score": 88.5
}
```

---

# 🧩 Chrome Extension Setup

1. Open Chrome
2. Go to:
   chrome://extensions/
3. Enable Developer Mode
4. Click “Load Unpacked”
5. Select `extension/`

---

# 📈 Future Improvements

* BERT & Transformer models
* Multi-language support
* Deep semantic verification
* Mobile application
* Social media integration
* Browser marketplace deployment

---

# 🔒 Security Notes

⚠️ Never upload:

* `.env`
* API keys
* `.pkl` model files

Use `.gitignore`:

```gitignore
.env
__pycache__/
*.pkl
```

---

# 🧪 Research & Technical Contributions

This project introduces a hybrid credibility detection framework by combining:

* Dataset-based classification
* Real-time external verification
* Contextual stance analysis

This improves real-world reliability compared to traditional single-model fake news systems.

---

# 👨‍💻 Authors

## Apoorv Prakash Gupta


- GitHub: https://github.com/Apoorv9554

---

## Thrista Dabas


- GitHub: https://github.com/Dabas04

# 📜 License

Licensed under the MIT License.

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository
🍴 Fork the repository
🛠️ Contribute improvements

---

<div align="center">

# 🚀 Building AI for Trustworthy Information

</div>
```
