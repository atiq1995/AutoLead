"""
Train a spam detector from datasets in "Spam Filtering/" and save
artifacts compatible with this project (scikit-learn 1.3.x).

Outputs:
- models/spam_detector.pkl
- models/vectorizer.pkl
"""
from __future__ import annotations

import os
import json
import logging
from pathlib import Path
from typing import List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


LOGGER = logging.getLogger("train_spam_detector")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "Spam Filtering"
MODELS_DIR = REPO_ROOT / "models"


def _read_smsspamcollection(path: Path) -> pd.DataFrame:
    # Typical format: label TAB message
    df = pd.read_csv(path, sep="\t", header=None, names=["label", "text"], encoding="utf-8", quoting=3)
    return df


def _read_emails_csv(path: Path) -> pd.DataFrame:
    # Try common schemas
    df = pd.read_csv(path)
    cols = {c.lower(): c for c in df.columns}
    # Heuristics for columns
    text_col = cols.get("text") or cols.get("message") or cols.get("content") or cols.get("body")
    label_col = cols.get("label") or cols.get("target") or cols.get("is_spam") or cols.get("spam")
    if not text_col or not label_col:
        # Fallback: try last column as label if binary, first string column as text
        text_col = text_col or df.select_dtypes(include=["object"]).columns[0]
        label_col = label_col or df.columns[-1]
    out = pd.DataFrame({"text": df[text_col].astype(str), "label": df[label_col]})
    # Normalize labels to {ham:0, spam:1}
    out["label"] = out["label"].apply(lambda v: 1 if str(v).strip().lower() in {"spam", "1", "true", "yes"} else 0)
    return out


def _read_enron_csv(path: Path) -> pd.DataFrame:
    # Reuse the generic CSV reader
    return _read_emails_csv(path)


def _load_datasets(base: Path) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []

    smsspam = base / "SMSSpamCollection"
    if smsspam.exists():
        LOGGER.info("Loading SMSSpamCollection ...")
        df = _read_smsspamcollection(smsspam)
        df["label"] = df["label"].map({"ham": 0, "spam": 1}).astype(int)
        frames.append(df)

    emails_csv = base / "emails.csv"
    if emails_csv.exists():
        LOGGER.info("Loading emails.csv ...")
        frames.append(_read_emails_csv(emails_csv))

    enron_csv = base / "enron_spam_data.csv"
    if enron_csv.exists():
        LOGGER.info("Loading enron_spam_data.csv ...")
        frames.append(_read_enron_csv(enron_csv))

    better_csv = base / "better30_cleaned.csv"
    if better_csv.exists():
        LOGGER.info("Loading better30_cleaned.csv ...")
        try:
            df = _read_emails_csv(better_csv)
            frames.append(df)
        except Exception as e:
            LOGGER.warning("Skipping better30_cleaned.csv: %s", e)

    # Custom labeled corpus: tab-separated with labels like "fraud" / "normal"
    fraud_file = base / "fraud_call.file"
    if fraud_file.exists():
        LOGGER.info("Loading fraud_call.file ...")
        try:
            df = pd.read_csv(fraud_file, sep="\t", header=None, names=["label", "text"], encoding="utf-8", quoting=3)
            df["label"] = df["label"].astype(str).str.strip().str.lower().map({
                "spam": 1,
                "fraud": 1,
                "ham": 0,
                "normal": 0,
            }).fillna(0).astype(int)
            frames.append(df)
        except Exception as e:
            LOGGER.warning("Skipping fraud_call.file: %s", e)

    if not frames:
        raise FileNotFoundError(
            "No supported datasets found in 'Spam Filtering/'. Expected one of: "
            "SMSSpamCollection, emails.csv, enron_spam_data.csv, better30_cleaned.csv"
        )

    data = pd.concat(frames, ignore_index=True)
    # Drop empties and duplicates
    data["text"] = data["text"].astype(str).str.strip()
    data = data.dropna(subset=["text"]).drop_duplicates(subset=["text"])\
               .reset_index(drop=True)
    return data[["text", "label"]]


def _augment_free_offer_samples(base: Path) -> pd.DataFrame:
    """Create additional spam samples focused on free-offer style language.

    Optionally reads `blacklist.json` for extra keywords and synthesizes examples.
    """
    phrases = [
        "congratulations you won a free prize claim now",
        "get your free gift card today limited time offer",
        "exclusive offer win cash now click the link",
        "free vacation package call immediately to claim",
        "limited time free upgrade act now",
        "you have been selected for a free reward",
        "free bonus waiting for you verify now",
        "win big prizes for free join today",
        "redeem your free voucher no purchase required",
        "free trial ends soon confirm your details",
        "maybe you might be interested in a free offer",
    ]

    # Optionally expand with blacklist keywords
    bl_path = base / "blacklist.json"
    if bl_path.exists():
        try:
            bl = json.loads(bl_path.read_text(encoding="utf-8"))
            kws = [k.strip() for k in bl.get("keywords", []) if isinstance(k, str) and k.strip()]
            for kw in kws:
                phrases.append(f"limited time {kw} offer act now")
                phrases.append(f"claim your free {kw} today")
        except Exception:
            pass

    return pd.DataFrame({
        "text": phrases,
        "label": [1] * len(phrases),
    })


def _build_vectorizer() -> TfidfVectorizer:
    # Word + char n-grams for robustness to obfuscation
    return TfidfVectorizer(
        strip_accents="unicode",
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        analyzer="word",
        max_features=5000,
    )


def train_and_save(data: pd.DataFrame, out_dir: Path) -> Tuple[Path, Path]:
    X_train, X_val, y_train, y_val = train_test_split(
        data["text"], data["label"], test_size=0.2, random_state=42, stratify=data["label"]
    )

    vectorizer = _build_vectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)

    model = LogisticRegression(max_iter=2000, n_jobs=None, class_weight="balanced")
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_val_vec)
    LOGGER.info("Validation report:\n%s", classification_report(y_val, y_pred, digits=3))

    out_dir.mkdir(parents=True, exist_ok=True)
    model_path = out_dir / "spam_detector.pkl"
    vec_path = out_dir / "vectorizer.pkl"
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)
    LOGGER.info("Saved model -> %s", model_path)
    LOGGER.info("Saved vectorizer -> %s", vec_path)
    return model_path, vec_path


def main() -> None:
    LOGGER.info("Loading datasets from: %s", DATA_DIR)
    data = _load_datasets(DATA_DIR)
    # Augment with free-offer spam samples
    aug = _augment_free_offer_samples(DATA_DIR)
    data = pd.concat([data, aug], ignore_index=True)
    LOGGER.info("Total samples: %d | Spam: %d | Ham: %d",
                len(data), int(data["label"].sum()), int((1 - data["label"]).sum()))
    train_and_save(data, MODELS_DIR)


if __name__ == "__main__":
    main()


