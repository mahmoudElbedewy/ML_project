from __future__ import annotations

import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import auc, roc_curve

from .config import FIGURE_DIR, METADATA_PATH, METRICS_PATH, MODEL_DIR, MODEL_PATHS, OUTPUT_DIR, RANDOM_STATE
from .data import data_counts, load_external_challenge, load_profile_data, load_reviewed_examples
from .features import normalize_text
from .modeling import (
    calculate_metrics,
    cluster_spam_messages,
    fit_final_pipeline,
    remove_duplicates,
    split_data,
    train_and_evaluate,
)


PROFILE_NAMES = {"sms": "SMS and alerts", "email": "Email", "jobs": "Job postings"}


# Save plots for the test results.
def _save_figures(profile: str, details: dict[str, object], clusters: pd.DataFrame) -> None:
    actual = details["y_test"]
    matrix = details["confusion_matrix"]
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks([0, 1], labels=["Ham", "Spam"])
    ax.set_yticks([0, 1], labels=["Ham", "Spam"])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"{PROFILE_NAMES[profile]} — Logistic Regression")
    for (row, column), value in np.ndenumerate(matrix):
        ax.text(column, row, str(value), ha="center", va="center", color="#17324D", fontsize=13)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{profile}_confusion_matrix.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    classifiers = [("Logistic Regression", details["logistic_probabilities"], details["pipeline"]["classifier"].classes_)]
    if details["knn_probabilities"] is not None:
        classifiers.append(("K-Nearest Neighbors", details["knn_probabilities"], ["ham", "spam"]))
    for name, probabilities, classes in classifiers:
        spam_index = list(classes).index("spam")
        false_positive, true_positive, _ = roc_curve(actual == "spam", probabilities[:, spam_index])
        ax.plot(false_positive, true_positive, label=f"{name} (AUC {auc(false_positive, true_positive):.3f})")
    ax.plot([0, 1], [0, 1], linestyle="--", color="#888888", label="Random reference")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve — {PROFILE_NAMES[profile]}")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{profile}_roc_curve.png", dpi=150)
    plt.close(fig)

    comparison = details["metrics"].set_index("model")
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    comparison["f1"].plot(kind="bar", color=["#0E7490", "#E58B42"][: len(comparison)], ax=ax)
    ax.set_ylim(0, 1)
    ax.set_ylabel("F1 score")
    ax.set_title(f"Model Comparison — {PROFILE_NAMES[profile]}")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{profile}_model_comparison.png", dpi=150)
    plt.close(fig)

    if not clusters.empty:
        fig, ax = plt.subplots(figsize=(7.2, 4.8))
        ax.bar(clusters["cluster"].astype(str), clusters["message_count"], color="#3977A8")
        ax.set_xlabel("Cluster number")
        ax.set_ylabel("Suspicious examples")
        ax.set_title(f"Unsupervised Text Groups — {PROFILE_NAMES[profile]}")
        ax.grid(axis="y", alpha=0.2)
        fig.tight_layout()
        fig.savefig(FIGURE_DIR / f"{profile}_clusters.png", dpi=150)
        plt.close(fig)


def _without_training_duplicates(external: pd.DataFrame, training: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    if external.empty:
        return external, 0
    training_keys = set(training["text"].map(normalize_text))
    external = external.copy()
    external["_key"] = external["text"].map(normalize_text)
    overlaps = external["_key"].isin(training_keys)
    removed = int(overlaps.sum())
    result = external.loc[~overlaps].drop(columns="_key").reset_index(drop=True)
    return result, removed


# Check the final model on separate data.
def _evaluate_external(
    profile: str,
    pipeline: dict[str, object],
    external: pd.DataFrame,
    metrics: list[dict[str, object]],
) -> dict[str, object]:
    if external.empty:
        return {"rows": 0}
    vectorizer = pipeline["vectorizer"]
    classifier = pipeline["classifier"]
    matrix = vectorizer.transform(external["text"].tolist())
    predictions = classifier.predict(matrix)
    probabilities = classifier.predict_proba(matrix)
    classes = list(classifier.classes_)
    positive_index = classes.index("spam")
    target = external["label"].to_numpy()

    if len(np.unique(target)) == 1:
        detected = int((predictions == "spam").sum())
        recall = float((predictions == "spam").mean())
        result = {"rows": int(len(external)), "spam_detected": detected, "recall": recall}
        metrics.append(
            {
                "profile": profile,
                "evaluation_set": "positive_only_external_challenge",
                "model": "Logistic Regression",
                "accuracy": np.nan,
                "precision": np.nan,
                "recall": recall,
                "f1": np.nan,
                "roc_auc": np.nan,
                "rows": len(external),
            }
        )
    else:
        result = {"rows": int(len(external)), **calculate_metrics(target, predictions, probabilities, classes)}
        metrics.append(
            {
                "profile": profile,
                "evaluation_set": "independent_external_test",
                "model": "Logistic Regression",
                **{key: result[key] for key in ("accuracy", "precision", "recall", "f1", "roc_auc")},
                "rows": len(external),
            }
        )

    pd.DataFrame(
        {
            "text": external["text"],
            "actual": target,
            "predicted": predictions,
            "spam_score": probabilities[:, positive_index],
        }
    ).to_csv(OUTPUT_DIR / f"{profile}_external_predictions.csv", index=False, encoding="utf-8-sig")
    return result


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading the SMS, email, and job-posting datasets...")
    raw_profiles = load_profile_data()
    metric_rows: list[dict[str, object]] = []
    summary: dict[str, object] = {"random_state": RANDOM_STATE, "profiles": {}}

    # Train one model for each text type.
    for profile, raw in raw_profiles.items():
        cleaned, removed = remove_duplicates(raw)
        if cleaned["label"].nunique() != 2 or cleaned["label"].value_counts().min() < 4:
            raise ValueError(f"بيانات {PROFILE_NAMES[profile]} لا تحتوي أمثلة كافية من الفئتين.")

        # Split the labeled rows for the model check.
        train, test = split_data(cleaned)
        compare_knn = profile in {"sms", "email"}
        print(
            f"{PROFILE_NAMES[profile]}: {len(cleaned):,} unique examples, "
            f"{len(train):,} train, {len(test):,} test."
        )
        print(f"Training Logistic Regression{' and KNN' if compare_knn else ''} on CPU...")
        # Train the models and score the test rows.
        details = train_and_evaluate(train, test, compare_knn=compare_knn)

        rows = details["metrics"].copy()
        rows.insert(0, "profile", profile)
        rows.insert(1, "evaluation_set", "stratified_test")
        rows["rows"] = len(test)
        metric_rows.extend(rows.to_dict(orient="records"))

        classes = list(details["pipeline"]["classifier"].classes_)
        positive_index = classes.index("spam")
        predictions = pd.DataFrame(
            {
                "text": test["text"],
                "source": test["source"],
                "actual": test["label"],
                "predicted": details["logistic_predictions"],
                "spam_score": details["logistic_probabilities"][:, positive_index],
            }
        )
        predictions.to_csv(OUTPUT_DIR / f"{profile}_test_predictions.csv", index=False, encoding="utf-8-sig")

        clusters = cluster_spam_messages(train.loc[train["label"] == "spam", "text"].tolist())
        clusters.to_csv(OUTPUT_DIR / f"{profile}_clusters.csv", index=False, encoding="utf-8-sig")
        _save_figures(profile, details, clusters)

        # Train the saved model on all labeled examples.
        final_data = pd.concat([cleaned, load_reviewed_examples(profile)], ignore_index=True)
        final_data, final_removed = remove_duplicates(final_data)
        final_pipeline = fit_final_pipeline(final_data)
        joblib.dump(final_pipeline, MODEL_PATHS[profile])

        external = load_external_challenge(profile)
        external, overlap_count = _without_training_duplicates(external, cleaned)
        external_summary = _evaluate_external(profile, final_pipeline, external, metric_rows)
        external_summary["training_overlaps_removed"] = overlap_count

        summary["profiles"][profile] = {
            "display_name": PROFILE_NAMES[profile],
            "raw_data": data_counts(raw),
            "clean_data": data_counts(cleaned),
            "duplicates_removed": int(removed),
            "training_rows": int(len(train)),
            "test_rows": int(len(test)),
            "feature_count": details["feature_count"],
            "final_model_rows": int(len(final_data)),
            "reviewed_examples_added": int(len(load_reviewed_examples(profile))),
            "model_path": str(MODEL_PATHS[profile]),
            "external_test": external_summary,
            "metrics": details["metrics"].to_dict(orient="records"),
        }

    # Save the scores and dataset details.
    pd.DataFrame(metric_rows).to_csv(METRICS_PATH, index=False, encoding="utf-8-sig")
    summary["limitations"] = [
        "The SMS translation collection is machine-translated from an English benchmark and is not native Egyptian SMS.",
        "The Arabic SMS source is small, so the SMS result should be treated as a classroom prototype.",
        "The bilingual email collection is small; its English external set is reported separately.",
        "The job postings are English-language examples; they do not represent the current Egyptian job market.",
        "Text-only scores cannot authenticate a sender or prove that a message is safe or fraudulent.",
    ]
    METADATA_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\nHeld-out results (higher is better):")
    print(pd.DataFrame(metric_rows).to_string(index=False, float_format=lambda value: f"{value:.4f}"))
    print("\nSaved three local models and their reports. The desktop app can now open offline.")
    print("Run: python -m src.gui_app")


if __name__ == "__main__":
    main()
