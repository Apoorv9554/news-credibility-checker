from pathlib import Path

import joblib
import numpy as np

_vectorizer = None
_model = None


def _force_single_thread(estimator) -> None:
    """
    Some persisted sklearn ensembles try to create worker pools during
    prediction, which can fail in restricted Windows environments.
    """
    if estimator is None:
        return

    if hasattr(estimator, "n_jobs"):
        try:
            estimator.n_jobs = 1
        except Exception:
            pass

    for attr in ("estimators_", "estimators"):
        children = getattr(estimator, attr, None)
        if not children:
            continue

        for child in children:
            nested = child[1] if isinstance(child, tuple) and len(child) == 2 else child
            _force_single_thread(nested)


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
    _force_single_thread(_model)
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

    try:
        X_vec = _vectorizer.transform([text])
        proba = _model.predict_proba(X_vec)[0][1]  # probability of label=1 (fake)
        return float(np.clip(proba, 0.0, 1.0))
    except Exception as exc:
        print(f"[fake_news_model] Prediction fallback triggered: {exc}")
        return 0.5
