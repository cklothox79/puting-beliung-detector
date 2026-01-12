# ==========================================================
# logger.py
# Logging Operasional Puting Beliung
# ==========================================================

import json
from pathlib import Path
from datetime import datetime

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

CSV_LOG = LOG_DIR / "realtime_log.csv"
JSON_LOG = LOG_DIR / "event_log.json"


# ==========================================================
# 1️⃣ LOG WAKTU-KE-WAKTU (CSV)
# ==========================================================
def log_realtime(decision_df, region_name):
    """
    Simpan keputusan realtime ke CSV
    """
    df = decision_df.copy()
    df["region"] = region_name
    df["logged_at"] = datetime.utcnow()

    if CSV_LOG.exists():
        df.to_csv(CSV_LOG, mode="a", header=False, index=False)
    else:
        df.to_csv(CSV_LOG, index=False)


# ==========================================================
# 2️⃣ LOG KEJADIAN SIGNIFIKAN (JSON)
# ==========================================================
def log_event(narrative, status, region_name):
    """
    Simpan event penting (WASPADA / PERINGATAN)
    """
    if status == "NORMAL":
        return

    event = {
        "time_utc": datetime.utcnow().isoformat(),
        "region": region_name,
        "status": status,
        "narrative": narrative
    }

    if JSON_LOG.exists():
        with open(JSON_LOG, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(event)

    with open(JSON_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
