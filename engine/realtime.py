# ==========================================================
#  REALTIME ENGINE – TERINTEGRASI DETECTOR
#  Module : engine/realtime.py
# ==========================================================

import pandas as pd
import random
from datetime import datetime
from engine.detector import run_detector

# ======================
# SAMPLE LOKASI
# ======================
WILAYAH_SAMPLE = [
    {"wilayah": "Sidoarjo", "lat": -7.45, "lon": 112.70},
    {"wilayah": "Gresik", "lat": -7.16, "lon": 112.65},
    {"wilayah": "Mojokerto", "lat": -7.47, "lon": 112.43},
    {"wilayah": "Pasuruan", "lat": -7.65, "lon": 112.90},
    {"wilayah": "Jombang", "lat": -7.55, "lon": 112.23},
]

# ======================
# LOAD REALTIME DATA
# ======================
def load_realtime_data():
    """
    Generate parameter atmosfer → detector → output peta
    """

    raw = []

    n_points = random.randint(1, 4)
    selected = random.sample(WILAYAH_SAMPLE, n_points)

    for loc in selected:
        raw.append({
            "wilayah": loc["wilayah"],
            "lat": loc["lat"] + random.uniform(-0.05, 0.05),
            "lon": loc["lon"] + random.uniform(-0.05, 0.05),
            "shear": round(random.uniform(5, 20), 1),      # knot
            "cape": int(random.uniform(300, 3000)),        # J/kg
            "cb_index": round(random.uniform(0.3, 0.9), 2) # indeks awan Cb
        })

    raw_df = pd.DataFrame(raw)

    detected_df = run_detector(raw_df)
    detected_df["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return detected_df
