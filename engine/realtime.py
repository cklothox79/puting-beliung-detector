# ======================================================
# realtime.py
# MODE OPERASIONAL - AUTO UPDATE
# Puting Beliung Detector
# ======================================================

import time
import json
import os
from datetime import datetime

from engine.reader import load_data
from engine.detector import detect_puting_beliung
from engine.narrator import generate_narration

# ===============================
# KONFIGURASI
# ===============================
INTERVAL_MINUTE = 10
OUTPUT_DIR = "output"
STATUS_FILE = os.path.join(OUTPUT_DIR, "latest_status.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===============================
# SATU SIKLUS ANALISIS
# ===============================
def run_cycle():
    print("\n▶ Mulai siklus deteksi...")

    ds = load_data()
    detection = detect_puting_beliung(ds)

    narration = generate_narration(detection)

    status = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "risk_level": detection["risk_level"],
        "risk_text": detection["risk_text"],
        "confidence": detection.get("confidence", 0),
        "narration": narration,
    }

    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)

    print("✓ Siklus selesai | Status:", status["risk_text"])

# ===============================
# LOOP OPERASIONAL
# ===============================
if __name__ == "__main__":
    print("🚀 PUTING BELIUNG DETECTOR")
    print("📡 MODE OPERASIONAL AKTIF")
    print(f"⏱ Update tiap {INTERVAL_MINUTE} menit")

    while True:
        try:
            run_cycle()
            time.sleep(INTERVAL_MINUTE * 60)

        except KeyboardInterrupt:
            print("\n⛔ Dihentikan manual")
            break

        except Exception as e:
            print("⚠ ERROR:", e)
            print("⏳ Coba lagi 1 menit...")
            time.sleep(60)
