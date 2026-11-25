from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from .config import (
    EMAIL_EXTERNAL_FILE,
    EMAIL_LEGIT_FILE,
    EMAIL_PHISHING_FILE,
    JOBS_TRAIN_FILE,
    REVIEWED_EXAMPLES_FILE,
    SMS_ARABIC_FILE,
    SMS_EXTERNAL_FILE,
    SMS_MULTILINGUAL_FILE,
)


ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
BASE_COLUMNS = ["text", "label", "source", "source_file", "profile", "group_id", "language"]


def _column_key(value: object) -> str:
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(value).lower())


def _read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    try:
        return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1", low_memory=False)


def _find_column(frame: pd.DataFrame, names: tuple[str, ...]) -> str | None:
    by_key = {_column_key(column): str(column) for column in frame.columns}
    return next((by_key[_column_key(name)] for name in names if _column_key(name) in by_key), None)


def _standardize_labels(values: pd.Series) -> pd.Series:
    positive = {"spam", "junk", "scam", "phishing", "phishingemail", "fraud", "fraudulent", "1", "10", "true", "yes"}
    negative = {"ham", "legitimate", "normal", "notspam", "nonscam", "safe", "safeemail", "0", "00", "false", "no"}

    def convert(value: object) -> str | None:
        key = _column_key(value)
        if key in positive:
            return "spam"
        if key in negative:
            return "ham"
        return None

    return values.map(convert)


def _has_arabic(value: object) -> bool:
    return bool(ARABIC_RE.search(str(value or "")))


def _language(value: str) -> str:
    has_arabic = _has_arabic(value)
    has_latin = bool(re.search(r"[A-Za-z]", value))
    if has_arabic and has_latin:
        return "Mixed"
    if has_arabic:
        return "Arabic"
    if has_latin:
        return "English"
    return "Unknown"


# Put each source into the same text and label format.
def _frame(rows: list[dict[str, object]]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=BASE_COLUMNS)
    result = pd.DataFrame(rows)
    for column in BASE_COLUMNS:
        if column not in result:
            result[column] = ""
    result["text"] = result["text"].fillna("").astype(str).str.strip()
    result["label"] = _standardize_labels(result["label"])
    result = result[(result["text"].str.len() > 0) & result["label"].notna()]
    return result[BASE_COLUMNS].reset_index(drop=True)


# Load the Arabic SMS examples.
def _load_sms_arabic() -> pd.DataFrame:
    if not SMS_ARABIC_FILE.exists():
        raise FileNotFoundError(f"ملف الرسائل العربية غير موجود: {SMS_ARABIC_FILE}")
    frame = _read_table(SMS_ARABIC_FILE)
    text_column = _find_column(frame, ("SMS", "message", "text"))
    label_column = _find_column(frame, ("Sentiment", "label", "class", "target"))
    if text_column is None or label_column is None:
        raise ValueError(f"أعمدة ملف الرسائل العربية غير متوقعة: {list(frame.columns)}")
    labels = _standardize_labels(frame[label_column])
    result = pd.DataFrame(
        {
            "text": frame[text_column].fillna("").astype(str).str.strip(),
            "label": labels,
            "source": "Arabic SMS corpus",
            "source_file": SMS_ARABIC_FILE.name,
            "profile": "sms",
            "group_id": [f"arabic-sms:{index}" for index in range(len(frame))],
            "language": "Arabic",
        }
    )
    return result[(result["text"].str.len() > 0) & result["label"].notna()].reset_index(drop=True)


# Keep Arabic rows from the translated SMS file.
def _load_sms_translations() -> pd.DataFrame:
    if not SMS_MULTILINGUAL_FILE.exists():
        raise FileNotFoundError(f"ملف الرسائل متعددة اللغات غير موجود: {SMS_MULTILINGUAL_FILE}")
    frame = _read_table(SMS_MULTILINGUAL_FILE)
    text_column = _find_column(frame, ("text_ar", "Arabic", "Arabic Text"))
    label_column = _find_column(frame, ("labels", "label", "class", "target"))
    if text_column is None or label_column is None:
        raise ValueError(f"أعمدة ملف الرسائل متعددة اللغات غير متوقعة: {list(frame.columns)}")
    labels = _standardize_labels(frame[label_column])
    text = frame[text_column].fillna("").astype(str).str.strip()
    group_column = _find_column(frame, ("Unnamed: 0", "id", "index"))
    groups = frame[group_column].fillna("").astype(str) if group_column else pd.Series(range(len(frame)), index=frame.index).astype(str)
    result = pd.DataFrame(
        {
            "text": text,
            "label": labels,
            "source": "Machine-translated SMS",
            "source_file": SMS_MULTILINGUAL_FILE.name,
            "profile": "sms",
            "group_id": "translated-sms:" + groups,
            "language": "Arabic (machine translated)",
        }
    )
    arabic_mask = result["text"].map(_has_arabic)
    return result[arabic_mask & (result["text"].str.len() > 0) & result["label"].notna()].reset_index(drop=True)


def load_sms_data() -> pd.DataFrame:
    return pd.concat([_load_sms_arabic(), _load_sms_translations()], ignore_index=True)


# Keep translated versions of one email in the same group.
def _load_bilingual_email_file(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"ملف الإيميلات غير موجود: {path}")
    frame = _read_table(path)
    id_column = _find_column(frame, ("No.", "No", "id", "number"))
    text_columns = [
        column
        for column in frame.columns
        if column != id_column and any(token in _column_key(column) for token in ("text", "message", "email"))
    ]
    if len(text_columns) < 2:
        raise ValueError(f"لم أجد حقلي النص العربي والإنجليزي في {path.name}: {list(frame.columns)}")

    rows: list[dict[str, object]] = []
    label_name = "spam" if label == "phishing" else "ham"
    for row_index, row in frame.iterrows():
        pair_number = row[id_column] if id_column else row_index
        for column in text_columns:
            text = str(row[column] or "").strip()
            if not text or text.lower() == "nan":
                continue
            rows.append(
                {
                    "text": text,
                    "label": label_name,
                    "source": "Bilingual email corpus",
                    "source_file": path.name,
                    "profile": "email",
                    "group_id": f"{label}:{pair_number}",
                    "language": _language(text),
                }
            )
    return _frame(rows)


def load_email_data() -> pd.DataFrame:
    legitimate = _load_bilingual_email_file(EMAIL_LEGIT_FILE, "legitimate")
    phishing = _load_bilingual_email_file(EMAIL_PHISHING_FILE, "phishing")
    return pd.concat([legitimate, phishing], ignore_index=True)


def load_email_external_test() -> pd.DataFrame:
    if not EMAIL_EXTERNAL_FILE.exists():
        return pd.DataFrame(columns=BASE_COLUMNS)
    frame = _read_table(EMAIL_EXTERNAL_FILE)
    text_column = _find_column(frame, ("Email Text", "text", "body", "message"))
    label_column = _find_column(frame, ("Email Type", "label", "class", "target"))
    if text_column is None or label_column is None:
        raise ValueError(f"أعمدة اختبار الإيميل غير متوقعة: {list(frame.columns)}")
    labels = _standardize_labels(frame[label_column])
    result = pd.DataFrame(
        {
            "text": frame[text_column].fillna("").astype(str).str.strip(),
            "label": labels,
            "source": "Independent English email set",
            "source_file": EMAIL_EXTERNAL_FILE.name,
            "profile": "email",
            "group_id": "",
            "language": "English",
        }
    )
    return result[(result["text"].str.len() > 0) & result["label"].notna()].reset_index(drop=True)


# Join the job fields into one text sample.
def load_jobs_data() -> pd.DataFrame:
    if not JOBS_TRAIN_FILE.exists():
        raise FileNotFoundError(f"ملف إعلانات الوظائف غير موجود: {JOBS_TRAIN_FILE}")
    frame = _read_table(JOBS_TRAIN_FILE)
    label_column = _find_column(frame, ("fraudulent", "label", "target"))
    if label_column is None:
        raise ValueError(f"لم أجد عمود تصنيف الوظائف fraudulent في {JOBS_TRAIN_FILE.name}")
    text_columns = [
        column
        for column in (
            "title", "location", "department", "salary_range", "company_profile", "description",
            "requirements", "benefits", "employment_type", "required_experience", "required_education",
            "industry", "function",
        )
        if column in frame.columns
    ]
    if not text_columns:
        raise ValueError(f"لم أجد حقول وصف الوظيفة في {JOBS_TRAIN_FILE.name}")
    text = frame[text_columns].fillna("").astype(str).agg(" ".join, axis=1).str.strip()
    return _frame(
        [
            {
                "text": text.iloc[index],
                "label": frame[label_column].iloc[index],
                "source": "Job postings",
                "source_file": JOBS_TRAIN_FILE.name,
                "profile": "jobs",
                "group_id": "",
                "language": "English",
            }
            for index in range(len(frame))
        ]
    )


def load_profile_data() -> dict[str, pd.DataFrame]:
    return {"sms": load_sms_data(), "email": load_email_data(), "jobs": load_jobs_data()}


# Load separate rows for an extra model check.
def load_external_challenge(profile: str) -> pd.DataFrame:
    if profile == "sms":
        if not SMS_EXTERNAL_FILE.exists():
            return pd.DataFrame(columns=BASE_COLUMNS)
        frame = _read_table(SMS_EXTERNAL_FILE)
        language_column = _find_column(frame, ("language", "lang"))
        text_column = _find_column(frame, ("text", "message", "translation"))
        if text_column is None:
            return pd.DataFrame(columns=BASE_COLUMNS)
        if language_column is not None:
            language = frame[language_column].fillna("").astype(str).str.lower().str.strip()
            frame = frame[language.isin({"arabic", "ar", "ara", "العربية"})]
            labels = pd.Series("spam", index=frame.index)
        else:
            frame = frame[frame[text_column].fillna("").astype(str).map(_has_arabic)]
            labels = pd.Series("spam", index=frame.index)
        result = pd.DataFrame(
            {
                "text": frame[text_column].fillna("").astype(str).str.strip(),
                "label": labels,
                "source": "External Arabic scam reports",
                "source_file": SMS_EXTERNAL_FILE.name,
                "profile": "sms",
                "group_id": "",
                "language": "Arabic",
            }
        )
        return result[result["text"].str.len() > 0].drop_duplicates("text").reset_index(drop=True)
    if profile == "email":
        return load_email_external_test()
    return pd.DataFrame(columns=BASE_COLUMNS)


# Add examples that were checked by a person.
def load_reviewed_examples(profile: str | None = None) -> pd.DataFrame:
    if not REVIEWED_EXAMPLES_FILE.exists():
        return pd.DataFrame(columns=BASE_COLUMNS)
    frame = _read_table(REVIEWED_EXAMPLES_FILE)
    text_column = _find_column(frame, ("text", "message", "sms"))
    label_column = _find_column(frame, ("label", "class", "target"))
    profile_column = _find_column(frame, ("profile", "channel", "domain"))
    if text_column is None or label_column is None:
        return pd.DataFrame(columns=BASE_COLUMNS)
    selected = frame.copy()
    selected["label"] = _standardize_labels(selected[label_column])
    selected["profile"] = selected[profile_column].fillna("sms").astype(str) if profile_column else "sms"
    if profile:
        selected = selected[selected["profile"] == profile]
    result = pd.DataFrame(
        {
            "text": selected[text_column].fillna("").astype(str).str.strip(),
            "label": selected["label"],
            "source": "User-reviewed examples",
            "source_file": REVIEWED_EXAMPLES_FILE.name,
            "profile": selected["profile"],
            "group_id": "",
            "language": selected[text_column].fillna("").astype(str).map(_language),
        }
    )
    return result[(result["text"].str.len() > 0) & result["label"].notna()].reset_index(drop=True)


def data_counts(frame: pd.DataFrame) -> dict[str, object]:
    if frame.empty:
        return {"rows": 0, "ham": 0, "spam": 0, "by_source": {}}
    counts = frame.groupby(["source", "label"], dropna=False).size().unstack(fill_value=0)
    source_counts = {
        str(source): {str(label): int(count) for label, count in row.items()}
        for source, row in counts.iterrows()
    }
    return {
        "rows": int(len(frame)),
        "ham": int((frame["label"] == "ham").sum()),
        "spam": int((frame["label"] == "spam").sum()),
        "by_source": source_counts,
    }
