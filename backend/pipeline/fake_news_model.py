from pathlib import Path
from typing import Optional

import joblib
import numpy as np

_vectorizer = None
_model = None


def _load_models_if_needed():
    """
    Lazy-loads the TF-IDF vectorizer and Logistic Regression model
    for fake news classification.
    """
    global _vectorizer, _model
    if _vectorizer is not None and _model is not None:
        return

    models_dir = Path(__file__).resolve().parents[1] / "models"
    vectorizer_path = models_dir / "fake_vectorizer.pkl"
    model_path = models_dir / "fake_model.pkl"

    if not vectorizer_path.exists() or not model_path.exists():
        print(
            "[fake_news_model] WARNING: Model files not found. "
            "Run ml/train_fake_news_model.py to train and save them."
        )
        _vectorizer = None
        _model = None
        return

    _vectorizer = joblib.load(vectorizer_path)
    _model = joblib.load(model_path)
    print("[fake_news_model] Loaded fake news vectorizer and model.")


def predict_fake_probability(text: str) -> float:
    """
    Returns the probability that the given text is fake news (0–1).

    If the model is not available, returns 0.5 as a neutral probability.
    """
    _load_models_if_needed()

    if _vectorizer is None or _model is None:
        # Model not trained or not found; neutral probability
        return 0.5

    X_vec = _vectorizer.transform([text])
    proba = _model.predict_proba(X_vec)[0][1]  # probability of label=1 (fake)
    return float(np.clip(proba, 0.0, 1.0))
