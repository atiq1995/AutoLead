## Spam Filtering: Training, Model, and Integration

This document explains how the new spam filtering pipeline works, how it is trained from the datasets inside `Spam Filtering/`, and how it integrates with the web app.

### Data Sources (in `Spam Filtering/`)
- `SMSSpamCollection` (label + text, tab-separated)
- `emails.csv`
- `enron_spam_data.csv`
- `better30_cleaned.csv`

Notes:
- Columns are auto-detected for CSVs (text/body/content vs label/target/is_spam).
- Labels are normalized to: ham = 0, spam = 1.
- Empty texts are dropped; duplicate messages are removed.

### Training Script
- Location: `scripts/train_spam_detector.py`
- What it does:
  - Loads all supported datasets from `Spam Filtering/`
  - Concatenates and cleans the data
  - Splits into train/validation (80/20, stratified)
  - Vectorizes text using TF‑IDF (word n‑grams 1–2, English stopwords, up to 5000 features)
  - Trains `LogisticRegression(max_iter=2000, class_weight="balanced")`
  - Prints a validation classification report
  - Saves artifacts to `models/spam_detector.pkl` and `models/vectorizer.pkl`

Augmentation:
- Adds a small set of synthetic "free offer" spam phrases to better capture promotional spam patterns.
- Optionally reads `Spam Filtering/blacklist.json` keywords and generates additional offer-like examples.

Run training:
```powershell
./venv/Scripts/python.exe scripts/train_spam_detector.py
```

Outputs:
- `models/spam_detector.pkl`
- `models/vectorizer.pkl`

These are automatically loaded by `src/spam_detector.py` on app startup.

### Inference & Threshold
- Inference uses the TF‑IDF vectorizer + Logistic Regression to compute spam probabilities.
- Classification threshold is configured via `.env` (default 0.7):
  - `SPAM_THRESHOLD=0.5` makes the detector more sensitive (more spam caught, potentially more false positives).

### Integration with the App
- The Flask app initializes `SpamDetector` from `src/spam_detector.py`.
- On startup, it loads `models/spam_detector.pkl` and `models/vectorizer.pkl` if present.
- If not found, it falls back to training a tiny default model (not recommended for production).

### Reproducibility & Demonstration Tips
- Keep datasets and training script in the repo.
- Save training logs:
  ```powershell
  ./venv/Scripts/python.exe scripts/train_spam_detector.py *>&1 | Tee-Object -FilePath reports/train_$(Get-Date -Format yyyyMMdd_HHmmss).txt
  ```
- Hash artifacts for verification:
  ```powershell
  Get-FileHash models\spam_detector.pkl, models\vectorizer.pkl
  ```
- Tag the commit after training:
  ```powershell
  git add .
  git commit -m "Train spam model from 'Spam Filtering' datasets"
  git tag -a v1-trained -m "Model trained from repo datasets"
  ```


