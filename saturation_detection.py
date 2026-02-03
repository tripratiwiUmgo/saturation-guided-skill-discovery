import numpy as np

# =========================
# Parameters (EXACT from paper)
# =========================
K = 10
R = 5
EPS_PRACTICAL = 0.05
EPS_NEAR = 0.01
COV_80 = 0.80
COV_90 = 0.90

def _coverage_index(cum_unique, threshold):
    idx = np.where(cum_unique >= threshold)[0]
    return int(idx[0] + 1) if len(idx) > 0 else np.nan

def detect_saturation_points(new_arr, cum_arr):
    final_unique = int(cum_arr[-1])

    if final_unique == 0 or len(new_arr) < K:
        return np.nan, np.nan, np.nan, np.nan, final_unique

    n80 = _coverage_index(cum_arr, COV_80 * final_unique)
    n90 = _coverage_index(cum_arr, COV_90 * final_unique)

    rolling_mdr = np.convolve(new_arr, np.ones(K) / K, mode="valid")

    def find_gated_saturation(rm, eps, gate):
        for i in range(len(rm) - R + 1):
            end_unit = i + K
            if end_unit < gate:
                continue
            if np.all(rm[i:i+R] <= eps):
                return end_unit
        return np.nan

    sat_practical = find_gated_saturation(rolling_mdr, EPS_PRACTICAL, n80)
    sat_near = find_gated_saturation(rolling_mdr, EPS_NEAR, n80)

    if sat_near == sat_practical:
        sat_near = np.nan

    return sat_practical, sat_near, n80, n90, final_unique
