# ==========================================================
#  DETECTOR CORE – PUTING BELIUNG
#  Module : engine/detector.py
# ==========================================================

import pandas as pd

# ======================
# PARAMETER AMBANG (AWAL)
# ======================
THRESHOLDS = {
    "shear": {
        "WASPADA": 8,
        "SIAGA": 12,
        "AWAS": 16
    },
    "cape": {
        "WASPADA": 500,
        "SIAGA": 1000,
        "AWAS": 2000
    },
    "cb_index": {
        "WASPADA": 0.4,
        "SIAGA": 0.6,
        "AWAS": 0.8
    }
}

# ======================
# HITUNG LEVEL
# ======================
def classify_level(shear, cape, cb_index):
    score = 0

    if shear >= THRESHOLDS["shear"]["AWAS"]:
        score += 3
    elif shear >= THRESHOLDS["shear"]["SIAGA"]:
        score += 2
    elif shear >= THRESHOLDS["shear"]["WASPADA"]:
        score += 1

    if cape >= THRESHOLDS["cape"]["AWAS"]:
        score += 3
    elif cape >= THRESHOLDS["cape"]["SIAGA"]:
        score += 2
    elif cape >= THRESHOLDS["cape"]["WASPADA"]:
        score += 1

    if cb_index >= THRESHOLDS["cb_index"]["AWAS"]:
        score += 3
    elif cb_index >= THRESHOLDS["cb_index"]["SIAGA"]:
        score += 2
    elif cb_index >= THRESHOLDS["cb_index"]["WASPADA"]:
        score += 1

    if score >= 7:
        return "AWAS"
    elif score >= 4:
        return "SIAGA"
    else:
        return "WASPADA"

# ======================
# DETECTION ENGINE
# ======================
def run_detector(input_df):
    """
    input_df minimal kolom:
    wilayah, lat, lon, shear, cape, cb_index
    """

    results = []

    for _, row in input_df.iterrows():
        level = classify_level(
            row["shear"],
            row["cape"],
            row["cb_index"]
        )

        results.append({
            "wilayah": row["wilayah"],
            "lat": row["lat"],
            "lon": row["lon"],
            "level": level,
            "shear": row["shear"],
            "cape": row["cape"],
            "cb_index": row["cb_index"],
            "keterangan": f"Shear={row['shear']} kt | CAPE={row['cape']} J/kg | CbIndex={row['cb_index']}"
        })

    return pd.DataFrame(results)
