from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion


_DIACRITICS = re.compile(r"[\u064b-\u065f\u0670]")
_URL = re.compile(r"(?:https?://|www\.)\S+", flags=re.IGNORECASE)
_EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
_NON_TEXT = re.compile(r"[^\w\s<>#@+:/.-]", flags=re.UNICODE)
_WHITESPACE = re.compile(r"\s+")


# Clean common text patterns before making features.
def normalize_text(text: object) -> str:
    value = str(text or "").lower()
    value = value.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))
    value = _URL.sub(" <url> ", value)
    value = _EMAIL.sub(" <email> ", value)
    value = _DIACRITICS.sub("", value).replace("ـ", "")
    value = value.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ؤ": "و", "ئ": "ي"}))
    value = _NON_TEXT.sub(" ", value)
    return _WHITESPACE.sub(" ", value).strip()


# Use words and character patterns as text features.
def build_vectorizer() -> FeatureUnion:
    word_features = TfidfVectorizer(
        preprocessor=normalize_text,
        lowercase=False,
        token_pattern=r"(?u)\b\w+\b",
        ngram_range=(1, 2),
        min_df=2,
        max_features=24000,
        sublinear_tf=True,
    )
    character_features = TfidfVectorizer(
        preprocessor=normalize_text,
        lowercase=False,
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=30000,
        sublinear_tf=True,
    )
    return FeatureUnion(
        [("word", word_features), ("char", character_features)],
        n_jobs=1,
    )
