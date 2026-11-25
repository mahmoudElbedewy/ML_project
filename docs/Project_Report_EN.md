# Text Safety and Job Posting Classifier

## Project overview

This local desktop application accepts three types of text: SMS or account alerts, emails, and job postings. The user chooses a category, pastes the text, and sees a model score, influential words, and results from the training experiment.

Each category has its own Logistic Regression model because SMS, email, and job advertisements have different writing patterns. The application is text-only and runs locally. It does not connect to Gmail, GitHub, banks, telecom providers, sender headers, or external links.

## Data used

- **SMS:** 494 Arabic messages from `Arabic_Spam.csv` and 5,489 non-empty Arabic rows from a multilingual collection containing 5,572 rows. The multilingual Arabic messages are machine translations from an English SMS benchmark, not native Egyptian messages. After duplicate removal, 5,291 texts remain: 4,535 Ham and 756 Spam.
- **Email:** 150 legitimate and 150 phishing bilingual records, each with two text fields. The legitimate file's language headers do not match the text language, so the loader identifies language from the content. Duplicate removal leaves 596 texts: 296 Ham and 300 Spam. Paired versions stay in the same split to avoid translation leakage.
- **Job postings:** 12,000 labeled English postings: 11,411 legitimate and 589 fraudulent. Text fields include title, company profile, description, requirements, benefits, and other listing information. Duplicate removal leaves 11,970 examples.

The separate SMS challenge contains 55 Arabic reported scams and no legitimate messages, so it supports recall only. The independent email check contains 2,000 English examples (1,000 safe and 1,000 phishing) and is not used for training. The Kaggle job test file is unlabeled and is not used for evaluation. See [dataset layout and source notes](DATA_LAYOUT.md).

## Method

The preprocessing step normalizes common Arabic letter forms and removes diacritics and tatweel. TF-IDF converts word and character patterns into numeric features. Logistic Regression is the main classifier for all three categories. K-Nearest Neighbors is compared with it on SMS and email. K-Means groups suspicious training examples to explore recurring text patterns; it does not produce the final risk classification.

The application evaluates each category on a held-out split. Email message pairs are assigned together to prevent paired translations from appearing in both train and test. Class imbalance in the job dataset is handled with balanced class weights. Metrics include accuracy, precision, recall, F1, ROC AUC, and the confusion matrix. R-squared is not appropriate because the target is categorical.

## Interpreting results

Scores indicate how the text resembles patterns in each model's training data. They are not calibrated probabilities of real-world fraud and do not authenticate the sender. A text-only model cannot verify whether a bank or service provider actually sent the message; that requires sender, URL, or email-header evidence.

The Arabic SMS data is limited and partly translated. Email and job datasets are in English and do not represent current Egyptian services or job postings. These limits should be stated in any presentation.

## Libraries

- `pandas` reads and organizes CSV data.
- `scikit-learn` handles TF-IDF, data splits, Logistic Regression, KNN, K-Means, and evaluation metrics.
- `matplotlib` creates confusion matrices, ROC curves, and model comparisons.
- `joblib` stores the trained models for local inference.
- `tkinter` provides the desktop interface.

## Run commands

```powershell
D:/PythonGlobal/global_venv/Scripts/Activate.ps1
cd D:/arabic_message_safety_project
python -m src.run_experiment
python -m src.gui_app
```

The app can be used offline after training. Its tabs, input text, and explanations have scrollbars for long content and smaller screens.
