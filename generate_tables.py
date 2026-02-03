import os
import pandas as pd

from extract_skills import load_units_csv, add_skills_column
from randomized_permutations import run_randomized_trials

DATA_DIR = "data"
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

JOBSTREET_PATH = f"{DATA_DIR}/job_units_clean.csv"
LINKEDIN_PATH = f"{DATA_DIR}/linkedin_unit_clean.csv"

def summarize(df, label):
    out = {}
    for col in ["sat_practical_units", "sat_near_units", "n80", "n90"]:
        out[f"{col}_mean"] = df[col].mean(skipna=True)
        out[f"{col}_sd"] = df[col].std(skipna=True)
        out[f"{col}_min"] = df[col].min(skipna=True)
        out[f"{col}_max"] = df[col].max(skipna=True)
    return pd.DataFrame(out, index=[label])

def main():
    df_js = add_skills_column(load_units_csv(JOBSTREET_PATH))
    df_li = add_skills_column(load_units_csv(LINKEDIN_PATH))

    metrics_js = run_randomized_trials(df_js, seed=7)
    metrics_li = run_randomized_trials(df_li, seed=13)

    summary = pd.concat([
        summarize(metrics_js, "JobStreet"),
        summarize(metrics_li, "LinkedIn")
    ])

    metrics_js.to_csv(f"{OUT_DIR}/table_runs_jobstreet.csv", index=False)
    metrics_li.to_csv(f"{OUT_DIR}/table_runs_linkedin.csv", index=False)
    summary.to_csv(f"{OUT_DIR}/table_summary_saturation.csv")

    print("\n=== Saturation Summary ===")
    print(summary)

if __name__ == "__main__":
    main()
