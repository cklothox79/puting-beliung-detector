# ======================================================
# app.py
# Dashboard Operasional Puting Beliung
# ======================================================

import streamlit as st
import json
import time
from datetime import datetime

STATUS_FILE = "output/latest_status.json"
REFRESH_SECOND = 30

st.set_page_config(
    page_title="Early Warning Puting Beliung",
    layout="centered"
)

st.title("🌪️ EARLY WARNING PUTING BELIUNG")
st.caption("BMKG – Sistem Operasional Otomatis")

placeholder = st.empty()

def load_status():
    with open(STATUS_FILE) as f:
        return json.load(f)

while True:
    with placeholder.container():
        try:
            status = load_status()

            # Header status
            st.subheader("Status Terkini")

            if status["risk_level"] == 2:
                st.error(status["risk_text"])
            elif status["risk_level"] == 1:
                st.warning(status["risk_text"])
            else:
                st.success(status["risk_text"])

            # Detail
            ts = datetime.fromisoformat(status["timestamp_utc"])
            st.write(f"🕒 Update terakhir: **{ts} UTC**")
            st.progress(status["confidence"] / 100)

            st.markdown("### Narasi Otomatis")
            st.info(status["narration"])

        except Exception as e:
            st.warning("Menunggu data dari engine...")
            st.caption(str(e))

    time.sleep(REFRESH_SECOND)
    st.experimental_rerun()
