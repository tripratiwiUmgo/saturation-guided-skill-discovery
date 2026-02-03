import re
import pandas as pd

# =========================
# Skill aliases
# =========================
SKILL_ALIASES = {
    "artificial intelligence": ["artificial intelligence", "ai", "kecerdasan buatan"],
    "machine learning": ["machine learning", "ml", "pembelajaran mesin"],
    "deep learning": ["deep learning"],
    "natural language processing": ["natural language processing", "nlp"],
    "computer vision": ["computer vision"],
    "python": ["python"],
    "sql": ["sql"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "cloud computing": ["cloud computing", "cloud"]
}

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

def build_patterns(skill_aliases):
    patterns = {}
    for skill, aliases in skill_aliases.items():
        escaped = [re.escape(a.lower()) for a in aliases]
        pat = r"(?<![A-Za-z0-9_])(" + "|".join(escaped) + r")(?![A-Za-z0-9_])"
        patterns[skill] = re.compile(pat, flags=re.IGNORECASE)
    return patterns

SKILL_PATTERNS = build_patterns(SKILL_ALIASES)

def extract_skills(text):
    t = text.lower()
    return {s for s, p in SKILL_PATTERNS.items() if p.search(t)}

def add_skills_column(df):
    df = df.copy()
    df["skills"] = df["text_clean"].apply(extract_skills)
    return df
