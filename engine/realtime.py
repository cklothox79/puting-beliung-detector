import time
import json
from datetime import datetime
from engine.reader import load_data
from engine.detector import detect_puting_beliung

INTERVAL_MINUTE = 10
OUTPUT_FILE = "output/latest_status.json"

def run_cycle():
    ds = load_data()
    result = detect_puting_beliung(ds)

    status = {
        "timestamp": datetime.utcnow().isoformat(),
        "risk_level": result["risk_level"],
        "risk_text": result["risk_text"],
        "confidence": result["confidence"]
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(status, f, indent=2)

    print("✓ Update:", status["risk_text"])

if __name__ == "__main__":
    print("🚀 REALTIME MODE AKTIF")
    while True:
        try:
            run_cycle()
            time.sleep(INTERVAL_MINUTE * 60)
        except Exception as e:
            print("⚠ ERROR:", e)
            time.sleep(60)
