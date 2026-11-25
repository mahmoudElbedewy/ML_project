from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
SMS_DIR = RAW_DIR / "sms"
EMAIL_DIR = RAW_DIR / "email"
JOBS_DIR = RAW_DIR / "jobs"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"

SMS_ARABIC_FILE = SMS_DIR / "arabic" / "Arabic_Spam.csv"
SMS_MULTILINGUAL_FILE = SMS_DIR / "multilingual" / "data-augmented.csv"
SMS_EXTERNAL_FILE = SMS_DIR / "external_test" / "final_dataset_output.csv"

EMAIL_LEGIT_FILE = EMAIL_DIR / "bilingual" / "legit-bilingual.csv"
EMAIL_PHISHING_FILE = EMAIL_DIR / "bilingual" / "phishing-bilingual.csv"
EMAIL_EXTERNAL_FILE = EMAIL_DIR / "external_test" / "Phishing_validation_emails.csv"

JOBS_TRAIN_FILE = JOBS_DIR / "job_postings_train.csv"
JOBS_UNLABELED_FILE = JOBS_DIR / "job_postings_test.csv"

REVIEWED_EXAMPLES_FILE = PROJECT_ROOT / "data" / "reviewed_examples.csv"
MODEL_PATHS = {
    "sms": MODEL_DIR / "sms_pipeline.joblib",
    "email": MODEL_DIR / "email_pipeline.joblib",
    "jobs": MODEL_DIR / "jobs_pipeline.joblib",
}

METRICS_PATH = OUTPUT_DIR / "metrics.csv"
METADATA_PATH = OUTPUT_DIR / "experiment_summary.json"
RANDOM_STATE = 42
TEST_SIZE = 0.25
