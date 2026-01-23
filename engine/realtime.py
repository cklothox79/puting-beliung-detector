# ==========================================================
#  REALTIME DATA ENGINE
#  Module : engine/realtime.py
# ==========================================================

import pandas as pd
import random
from datetime import datetime

# ======================
# KONFIGURASI
# ======================
WILAYAH_SAMPLE = [
    {"wilayah": "Sidoarjo", "lat": -7.45, "lon": 112.70},
    {"wilayah": "Gresik", "lat": -7.16, "lon": 112.65},
    {"wilayah": "Mojokerto", "lat": -7.47, "lon": 112.43},
    {"wilayah": "Pasuruan", "lat": -7.65, "lon": 112.90},
    {"wilayah": "Jombang", "lat": -7.55, "lon": 112.23},
]

LEVELS = ["WASPADA", "SIAGA", "AWAS"]

KETERANGAN = {
    "WASPADA": "Pertumbuhan awan Cb terpantau",
    "SIAGA": "Shear rendah dan konvergensi terdeteksi",
    "AWAS": "Indikasi kuat puting beliung"
}

# ======================
# GENERATE DATA REALTIME
# ======================
def load_realtime_data():
    """
    Menghasilkan data realtime indikasi puting beliung
    (versi simulasi operasional)
    """

    data = []

    # Jumlah titik aktif (acak tapi realistis)
    n_points = random.randint(1, 4)

    selected = random.sample(WILAYAH_SAMPLE, n_points)

    for loc in selected:
        level = random.choices(
            LEVELS,
            weights=[0.5, 0.3, 0.2],
            k=1
        )[0]

        data.append({
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            "wilayah": loc["wilayah"],
            "lat": loc["lat"] + random.uniform(-0.05, 0.05),
            "lon": loc["lon"] + random.uniform(-0.05, 0.05),
            "level": level,
            "keterangan": KETERANGAN[level]
        })

    df = pd.DataFrame(data)

    return df
