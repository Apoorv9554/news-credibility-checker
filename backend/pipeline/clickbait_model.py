from pathlib import Path

import joblib
import numpy as np

_vectorizer = None
_model = None


def _force_single_thread(estimator) -> None:
    """
    Keep persisted sklearn estimators on a single thread so prediction
    stays compatible with restricted Windows environments.
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
    for clickbait detection.
    """
    global _vectorizer, _model
    if _vectorizer is not None and _model is not None:
        return

    models_dir = Path(__file__).resolve().parents[1] / "models"
    vectorizer_path = models_dir / "clickbait_vectorizer.pkl"
    model_path = models_dir / "clickbait_model.pkl"

    if not vectorizer_path.exists() or not model_path.exists():
        print(
            "[clickbait_model] WARNING: Model files not found. "
            "Run ml/train_clickbait_model.py to train and save them."
        )
        _vectorizer = None
        _model = None
        return

    _vectorizer = joblib.load(vectorizer_path)
    _model = joblib.load(model_path)
    _force_single_thread(_model)
    print("[clickbait_model] Loaded clickbait vectorizer and model.")


def predict_clickbait_score(headline: str) -> float:
    """
    Returns a score in [0, 1] where:
        1.0 => very likely NON-clickbait
        0.0 => very likely clickbait

    If the model is not available, returns 0.7 as a default.
    """
    _load_models_if_needed()

    if _vectorizer is None or _model is None:
        # Default fallback if not trained yet
        return 0.7

    if not headline.strip():
        return 0.7

    try:
        X_vec = _vectorizer.transform([headline])
        # We trained the model so that label 1 = NON-clickbait
        proba_non_clickbait = _model.predict_proba(X_vec)[0][1]
        return float(np.clip(proba_non_clickbait, 0.0, 1.0))
    except Exception as exc:
        print(f"[clickbait_model] Prediction fallback triggered: {exc}")
        return 0.7
