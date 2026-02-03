import re
import pandas as pd

# =========================
# Skill aliases (UPDATED)
# =========================
SKILL_ALIASES = {
    "artificial intelligence": ["artificial intelligence", "ai", "kecerdasan buatan"],
    "machine learning": ["machine learning", "ml", "pembelajaran mesin"],
    "deep learning": ["deep learning", "pembelajaran mendalam"],
    "natural language processing": [
        "natural language processing", "nlp", "pemrosesan bahasa alami"
    ],
    "computer vision": ["computer vision", "visi komputer"],

    "data analysis": ["data analysis", "analisis data"],
    "data processing": ["data processing", "pengolahan data"],
    "data pipeline": ["data pipeline", "pipeline data", "alur data"],
    "feature engineering": ["feature engineering", "rekayasa fitur"],
    "predictive analytics": ["predictive analytics", "analitik prediktif"],

    "python": ["python"],
    "sql": ["sql"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "go": ["go", "golang"],

    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "hugging face": ["hugging face"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],

    "large language model": ["large language model", "llm", "model bahasa besar"],
    "retrieval augmented generation": [
        "rag", "retrieval augmented generation"
    ],
    "prompt engineering": ["prompt engineering", "rekayasa prompt"],

    "cloud computing": ["cloud", "cloud computing", "komputasi awan"],
    "aws": ["aws", "amazon web services"],
    "gcp": ["gcp", "google cloud"],
    "azure": ["azure", "microsoft azure"],

    "mlops": ["mlops"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "ci/cd": [
        "ci/cd", "continuous integration", "continuous deployment"
    ],

    "api": ["api", "antarmuka pemrograman aplikasi"],
    "rest api": ["rest api"],
    "microservices": ["microservices", "layanan mikro"],
}

# =========================
# CSV loader
# =========================
REQUIRED_COLS = ["unit_id", "job_id", "platform", "section", "text"]

def load_units_csv(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    df = df[REQUIRED_COLS].copy()
    df["text_clean"] = (
        df["text"].astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    return df

# =========================
# Skill extraction
# =========================
def build_patterns(skill_aliases):
    patterns = {}
    for skill, aliases in skill_aliases.items():
        escaped = [re.escape(a.lower()) for a in aliases]
        pattern = r"(?<![A-Za-z0-9_])(" + "|".join(escaped) + r")(?![A-Za-z0-9_])"
        patterns[skill] = re.compile(pattern, flags=re.IGNORECASE)
    return patterns

SKILL_PATTERNS = build_patterns(SKILL_ALIASES)

def extract_skills(text):
    t = text.lower()
    return {skill for skill, pat in SKILL_PATTERNS.items() if pat.search(t)}

def add_skills_column(df):
    df = df.copy()
    df["skills"] = df["text_clean"].apply(extract_skills)
    return df
