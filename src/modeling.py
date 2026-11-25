from __future__ import annotations

from collections import defaultdict

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier

from .config import RANDOM_STATE, TEST_SIZE
from .features import build_vectorizer, normalize_text


# Remove repeated text and labels that disagree.
def remove_duplicates(frame: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    original_count = len(frame)
    result = frame.copy()
    result["normalized_text"] = result["text"].map(normalize_text)
    result = result[result["normalized_text"].str.len() > 0]
    conflicts = result.groupby("normalized_text")["label"].nunique()
    conflicting_texts = set(conflicts[conflicts > 1].index)
    result = result[~result["normalized_text"].isin(conflicting_texts)]
    result = result.drop_duplicates("normalized_text", keep="first").reset_index(drop=True)
    return result.drop(columns="normalized_text"), original_count - len(result)


# Keep paired email versions on the same side of the split.
def split_data(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    groups = frame.get("group_id")
    if groups is not None and groups.fillna("").astype(str).str.len().gt(0).all():
        splitter = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)
        train_indices, test_indices = next(
            splitter.split(np.zeros(len(frame)), frame["label"], groups=groups.astype(str))
        )
    else:
        indices = np.arange(len(frame))
        train_indices, test_indices = train_test_split(
            indices,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=frame["label"],
        )
    return frame.iloc[train_indices].reset_index(drop=True), frame.iloc[test_indices].reset_index(drop=True)


# Calculate scores from the test labels and predictions.
def calculate_metrics(y_test: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray, classes: list[str]) -> dict[str, float]:
    spam_index = classes.index("spam")
    spam_scores = y_prob[:, spam_index]
    actual_positive = y_test == "spam"
    predicted_positive = y_pred == "spam"
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(actual_positive, predicted_positive, zero_division=0)),
        "recall": float(recall_score(actual_positive, predicted_positive, zero_division=0)),
        "f1": float(f1_score(actual_positive, predicted_positive, zero_division=0)),
        "roc_auc": float(roc_auc_score(actual_positive, spam_scores)),
    }


# Train the main Logistic Regression model.
def _fit_logistic(X_train, y_train: np.ndarray) -> LogisticRegression:
    model = LogisticRegression(
        max_iter=1200,
        class_weight="balanced",
        C=2.0,
        solver="liblinear",
        random_state=RANDOM_STATE,
    )
    model.fit(X_train, y_train)
    return model


# Train the models and compare their test results.
def train_and_evaluate(
    train: pd.DataFrame,
    test: pd.DataFrame,
    compare_knn: bool = False,
) -> dict[str, object]:
    vectorizer = build_vectorizer()
    # Learn text features from training data only.
    X_train = vectorizer.fit_transform(train["text"].tolist())
    X_test = vectorizer.transform(test["text"].tolist())
    y_train = train["label"].to_numpy()
    y_test = test["label"].to_numpy()

    model = _fit_logistic(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)
    classes = list(model.classes_)
    rows = [{"model": "Logistic Regression", **calculate_metrics(y_test, y_pred, y_prob, classes)}]
    knn_pred = None
    knn_prob = None

    if compare_knn:
        knn = KNeighborsClassifier(
            n_neighbors=min(5, len(train)),
            weights="distance",
            metric="cosine",
            algorithm="brute",
            n_jobs=-1,
        )
        # Compare a weighted KNN with the main model.
        knn.fit(X_train, y_train)
        knn_pred = knn.predict(X_test)
        knn_prob = knn.predict_proba(X_test)
        rows.append({"model": "K-Nearest Neighbors", **calculate_metrics(y_test, knn_pred, knn_prob, list(knn.classes_))})

    return {
        "pipeline": {"vectorizer": vectorizer, "classifier": model, "classes": model.classes_},
        "y_test": y_test,
        "logistic_predictions": y_pred,
        "logistic_probabilities": y_prob,
        "knn_predictions": knn_pred,
        "knn_probabilities": knn_prob,
        "metrics": pd.DataFrame(rows),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=["ham", "spam"]),
        "feature_count": int(X_train.shape[1]),
    }


# Train the final model on all labeled examples.
def fit_final_pipeline(frame: pd.DataFrame) -> dict[str, object]:
    vectorizer = build_vectorizer()
    X = vectorizer.fit_transform(frame["text"].tolist())
    y = frame["label"].to_numpy()
    model = _fit_logistic(X, y)
    return {"vectorizer": vectorizer, "classifier": model, "classes": model.classes_}


# Group similar spam examples to inspect common patterns.
def cluster_spam_messages(texts: list[str], cluster_count: int = 5) -> pd.DataFrame:
    if len(texts) < 2:
        return pd.DataFrame(columns=["cluster", "message_count", "top_terms"])

    vectorizer = TfidfVectorizer(
        preprocessor=normalize_text,
        lowercase=False,
        token_pattern=r"(?u)\b\w+\b",
        ngram_range=(1, 2),
        min_df=2,
        max_features=12000,
        sublinear_tf=True,
    )
    X = vectorizer.fit_transform(texts)
    if X.shape[1] == 0:
        return pd.DataFrame(columns=["cluster", "message_count", "top_terms"])

    cluster_count = min(cluster_count, len(texts))
    kmeans = KMeans(n_clusters=cluster_count, random_state=RANDOM_STATE, n_init=5, max_iter=100)
    clusters = kmeans.fit_predict(X)
    terms = vectorizer.get_feature_names_out()
    rows = []
    for cluster_id, center in enumerate(kmeans.cluster_centers_):
        top = center.argsort()[-8:][::-1]
        rows.append(
            {
                "cluster": int(cluster_id),
                "message_count": int((clusters == cluster_id).sum()),
                "top_terms": ", ".join(terms[index] for index in top if center[index] > 0),
            }
        )
    return pd.DataFrame(rows).sort_values("cluster").reset_index(drop=True)


# Show which words moved the score up or down.
def explain_message(pipeline: dict[str, object], text: str, limit: int = 5) -> dict[str, list[tuple[str, float]]]:
    vectorizer = pipeline["vectorizer"]
    classifier = pipeline["classifier"]
    X = vectorizer.transform([text])
    names = vectorizer.get_feature_names_out()
    classes = list(classifier.classes_)
    positive_index = classes.index("spam")
    coefficients = classifier.coef_[positive_index]
    active = X.tocoo()
    accumulated: dict[str, float] = defaultdict(float)

    for column, value in zip(active.col, active.data):
        name = names[column]
        if not name.startswith("word__"):
            continue
        term = name[len("word__"):].replace("_", " ").strip()
        if term:
            accumulated[term] += float(value * coefficients[column])

    ranked = sorted(accumulated.items(), key=lambda item: item[1], reverse=True)
    return {
        "spam": [(term, score) for term, score in ranked if score > 0][:limit],
        "ham": [(term, score) for term, score in reversed(ranked) if score < 0][:limit],
    }
