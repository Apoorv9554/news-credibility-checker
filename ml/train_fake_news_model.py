import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import re

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import VotingClassifier


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def load_dataset() -> pd.DataFrame:

    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"

    fake_path = data_dir / "Fake.csv"
    true_path = data_dir / "True.csv"

    if not fake_path.exists() or not true_path.exists():
        raise FileNotFoundError(
            f"Expected Fake.csv and True.csv in {data_dir}"
        )

    df_fake = pd.read_csv(fake_path)
    df_true = pd.read_csv(true_path)

    if "text" not in df_fake.columns or "text" not in df_true.columns:
        raise KeyError("Expected a 'text' column in dataset")

    df_fake["label"] = 1
    df_true["label"] = 0

    df = pd.concat([
        df_fake[["title", "text", "label"]],
        df_true[["title", "text", "label"]]
    ])

    df = df.dropna(subset=["text"])

    return df


def train_and_save_model():

    print("Loading dataset...")
    df = load_dataset()

    print(f"Total samples: {len(df)}")
    print(df["label"].value_counts())

    X = (df["title"] + " " + df["text"]).astype(str).apply(clean_text)
    y = df["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Vectorizing text with TF-IDF...")

    vectorizer = TfidfVectorizer(
        max_features=30000,
        ngram_range=(1,2),
        stop_words="english",
        min_df=2,
        max_df=0.9,
        sublinear_tf=True
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Creating ensemble models...")

    lr = LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    )

    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    svm = SGDClassifier(loss="log_loss")

    ensemble_model = VotingClassifier(
    estimators=[
        ("lr", lr),
        ("rf", rf),
        ("svm", svm)
    ],
    voting="soft"
    )

    print("Training ensemble model...")
    ensemble_model.fit(X_train_vec, y_train)

    print("Evaluating on test set...")

    y_pred = ensemble_model.predict(X_test_vec)

    acc = accuracy_score(y_test, y_pred)

    print(f"Test Accuracy: {acc:.4f}")
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    project_root = Path(__file__).resolve().parents[1]
    models_dir = project_root / "backend" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    vectorizer_path = models_dir / "fake_vectorizer.pkl"
    model_path = models_dir / "fake_model.pkl"

    print(f"Saving vectorizer to: {vectorizer_path}")
    print(f"Saving model to: {model_path}")

    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(ensemble_model, model_path)

    print("Training complete and models saved.")


if __name__ == "__main__":
    train_and_save_model()