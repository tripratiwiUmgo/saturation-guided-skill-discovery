import numpy as np

def compute_discovery_curves(df):
    seen = set()
    new_per_unit = []
    cumulative_unique = []

    for skills in df["skills"]:
        new = skills - seen
        new_per_unit.append(len(new))
        seen |= skills
        cumulative_unique.append(len(seen))

    return np.array(new_per_unit), np.array(cumulative_unique)
