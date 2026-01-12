# ==========================================================
# realtime.py
# Realtime Engine Puting Beliung
# Versi: BMKG Operasional
# ==========================================================

import time
from datetime import datetime

from engine.reader import read_sample_data
from engine.preprocessor import preprocess_satellite
from engine.indices import calculate_indices
from engine.detector import run_detection
from engine.narrator import generate_full_narrative


# ==========================================================
# PARAMETER OPERASIONAL
# ==========================================================
INTERVAL_MINUTES = 10
REGION_NAME = "wilayah kajian"


# ==========================================================
# 1️⃣ SATU SIKLUS DETEKSI
# ==========================================================
def run_cycle():
    print("=" * 60)
    print(f"⏱️ Realtime Cycle | {datetime.utcnow()} UTC")

    # 1. READ DATA (sementara mock)
    ds = read_sample_data()

    # 2. PREPROCESS
    ds = preprocess_satellite(ds)

    # 3. INDICES
    ds = calculate_indices(ds)

    # 4. DETECTION
    detection = run_detection(ds)

    # 5. NARRATION
    narasi = generate_full_narrative(
        detection,
        region_name=REGION_NAME
    )

    print("\n📢 NARASI OTOMATIS:")
    print(narasi)

    return detection


# ==========================================================
# 2️⃣ LOOP REALTIME
# ==========================================================
def start_realtime():
    print("🚀 Realtime Puting Beliung Engine STARTED")
    print(f"⏲️ Interval: {INTERVAL_MINUTES} menit\n")

    while True:
        try:
            run_cycle()
        except Exception as e:
            print("❌ ERROR:", e)

        time.sleep(INTERVAL_MINUTES * 60)


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    start_realtime()
