# FitWise AI — Personalized Size & Fit Recommendation

A student-project prototype that ranks available clothing sizes using body measurements, product size charts, and fit preferences. It also includes an optional scikit-learn model for learning historical `small` / `fit` / `large` feedback.

## Features
- Flask web application with responsive interface
- Sample catalog and SQLite persistence
- Unit conversion from inches to centimetres
- Transparent measurement-ease ranking
- Optional feedback collection
- Optional ML training pipeline and metrics report
- Automated tests for the baseline recommender

## Important data note
The products and size-chart measurements seeded by this project are illustrative demo values, not verified manufacturer measurements. Replace them with verified product-specific size charts before making real-world claims. The recommendation logic is a baseline and does not guarantee fit.

## Requirements
- Python 3.10+
- VS Code recommended

## Setup (Windows PowerShell)
```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```
Open the local address printed by Flask, normally `http://127.0.0.1:5000`.

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

## Run tests
```bash
python -m pytest
```

## Optional ML training
1. Download the clothing fit dataset from Kaggle: https://www.kaggle.com/datasets/rmisra/clothing-fit-dataset-for-size-recommendation
2. Put the JSON or CSV dataset in `data/`. Keep the original data license and attribution.
3. Inspect its columns before training.
4. Run:
```bash
python -m src.ml.train_model --data data/modcloth_final_data.json
```
The script saves `models/fit_classifier.joblib` and a JSON metrics report. The model is an optional training artifact and is not used by the baseline website yet. It predicts fit feedback from the supported fields in the dataset, not a universally correct garment size. Verify the actual columns and evaluate for leakage and class imbalance before interpreting the metrics.

## Database
The SQLite database `fitwise.db` is created automatically on first run. Delete it only if you want to reset the demo catalog and feedback; it will be recreated on next launch.

## Folder layout
```text
fitwise-ai/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
├── models/
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── recommender.py
│   └── ml/
│       ├── __init__.py
│       ├── train_model.py
│       └── predict.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   └── about.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── tests/test_recommender.py
```

## Next improvements
- Add admin CRUD screens for products and size charts.
- Validate ease thresholds separately for each garment category and measurement convention.
- Use group-based train/test splits by customer or product to reduce leakage.
- Add confidence calibration and monitoring before exposing probabilities to users.
- Add optional virtual try-on only as a separately evaluated feature.
- Before public deployment, set a strong secret key, turn off Flask debug mode, add CSRF protection, validate all inputs server-side, and review privacy/security.
