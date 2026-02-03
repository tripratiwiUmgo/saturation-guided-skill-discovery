import numpy as np
import pandas as pd

from compute_discovery_curves import compute_discovery_curves
from saturation_detection import detect_saturation_points

N_RUNS = 30

def run_randomized_trials(df, seed):
    rng = np.random.default_rng(seed)
    rows = []

    for r in range(N_RUNS):
        df_shuffled = df.sample(
            frac=1,
            random_state=rng.integers(1_000_000_000)
        ).reset_index(drop=True)

        new_arr, cum_arr = compute_discovery_curves(df_shuffled)

        sat_p, sat_n, n80, n90, fu = detect_saturation_points(
            new_arr, cum_arr
        )

        rows.append({
            "run": r + 1,
            "sat_practical_units": sat_p,
            "sat_near_units": sat_n,
            "n80": n80,
            "n90": n90,
            "final_unique_skills": fu,
            "N_units": len(df)
        })

    return pd.DataFrame(rows)
