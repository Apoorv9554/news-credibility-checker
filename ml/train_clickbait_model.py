import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib


def load_clickbait_dataset() -> pd.DataFrame:
    """
    Loads clickbait_data.csv from ./data and returns a DataFrame
    with columns: headline, label_clean

    Assumes:
    - There is a text column for the headline: one of
      ['headline', 'title', 'Headline', 'Title']
    - There is a label column where:
        1 = clickbait
        0 = non-clickbait

    We convert it so:
        label_clean = 1 => NON-clickbait
        label_clean = 0 => clickbait
    """
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    csv_path = data_dir / "clickbait_data.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Expected {csv_path} to exist.")

    df = pd.read_csv(csv_path)

    # Find headline column
    headline_col = None
    for col in ["headline", "title", "Headline", "Title"]:
        if col in df.columns:
            headline_col = col
            break

    if headline_col is None:
        raise KeyError(
            "Expected a headline/title column in clickbait_data.csv. "
            "Tried: 'headline', 'title', 'Headline', 'Title'. "
            f"Found columns: {df.columns}"
        )

    # Find label column
    label_col = None
    for col in ["label", "clickbait", "is_clickbait"]:
        if col in df.columns:
            label_col = col
            break

    if label_col is None:
        raise KeyError(
            "Expected a label column in clickbait_data.csv. "
            "Tried: 'label', 'clickbait', 'is_clickbait'. "
            f"Found columns: {df.columns}"
        )

    df = df[[headline_col, label_col]].dropna()
    df = df.rename(columns={headline_col: "headline", label_col: "label_raw"})

    # Ensure labels are 0/1
    df["label_raw"] = df["label_raw"].astype(int)

    # IMPORTANT:
    # Assume label_raw: 1 = clickbait, 0 = non-clickbait
    # We invert so:
    #   label_clean = 1 => NON-clickbait
    #   label_clean = 0 => clickbait
    df["label_clean"] = 1 - df["label_raw"]

    return df[["headline", "label_clean"]]


def train_and_save_clickbait_model():
    print("Loading clickbait dataset...")
    df = load_clickbait_dataset()
    print(f"Total samples: {len(df)}")
    print(df["label_clean"].value_counts())

    X = df["headline"].astype(str)
    y = df["label_clean"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Vectorizing headlines with TF-IDF...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        stop_words="english"
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Logistic Regression model (single process)...")
    model = LogisticRegression(max_iter=2000)
    model.fit(X_train_vec, y_train)

    print("Evaluating on test set...")
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.4f}")
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    # Save vectorizer and model in backend/models
    project_root = Path(__file__).resolve().parents[1]
    models_dir = project_root / "backend" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    vectorizer_path = models_dir / "clickbait_vectorizer.pkl"
    model_path = models_dir / "clickbait_model.pkl"

    print(f"Saving clickbait vectorizer to: {vectorizer_path}")
    print(f"Saving clickbait model to: {model_path}")

    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(model, model_path)

    print("Clickbait model training complete and models saved.")


if __name__ == "__main__":
    train_and_save_clickbait_model()
