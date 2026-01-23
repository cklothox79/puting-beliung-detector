# ==========================================================
#  PUTING BELIUNG DETECTOR – DASHBOARD OPERASIONAL
#  Repo  : puting-beliung-detector
#  Mode  : Realtime Monitoring
#  Author: Tim Operasional
# ==========================================================

import streamlit as st
from visualization.plotter import render_realtime_map
from engine.realtime import load_realtime_data
from engine.logger import setup_logger

# ======================
# CONFIG DASAR
# ======================
st.set_page_config(
    page_title="Puting Beliung Detector",
    page_icon="🌪️",
    layout="wide"
)

logger = setup_logger()

# ======================
# SIDEBAR
# ======================
st.sidebar.title("🌪️ Puting Beliung Detector")
st.sidebar.caption("Mode Operasional • Realtime")

st.sidebar.markdown("---")

interval = st.sidebar.selectbox(
    "⏱️ Interval Update (detik)",
    options=[30, 60, 120, 300],
    index=1
)

show_map = st.sidebar.checkbox("🗺️ Tampilkan Peta", value=True)
show_table = st.sidebar.checkbox("📋 Tampilkan Tabel Data", value=True)

st.sidebar.markdown("---")
st.sidebar.caption("BMKG Style Early Warning")

# ======================
# AUTO REFRESH
# ======================
st.experimental_autorefresh(
    interval=interval * 1000,
    key="auto_refresh_dashboard"
)

# ======================
# HEADER
# ======================
st.title("🌪️ Dashboard Realtime Deteksi Puting Beliung")
st.markdown(
    """
    **Sistem pemantauan berbasis analisis dinamika atmosfer & satelit.**  
    Update otomatis sesuai interval operasional.
    """
)

# ======================
# LOAD DATA REALTIME
# ======================
try:
    df_realtime = load_realtime_data()
    logger.info("Realtime data loaded successfully")
except Exception as e:
    st.error("Gagal memuat data realtime")
    logger.error(f"Realtime load error: {e}")
    df_realtime = None

# ======================
# LAYOUT UTAMA
# ======================
if show_map:
    st.subheader("🗺️ Peta Realtime Wilayah Terindikasi")

    render_realtime_map(
        realtime_df=df_realtime,
        height=600
    )

# ======================
# TABEL DATA
# ======================
if show_table:
    st.subheader("📋 Data Realtime Deteksi")

    if df_realtime is not None and not df_realtime.empty:
        st.dataframe(
            df_realtime,
            use_container_width=True
        )
    else:
        st.info("Belum ada data indikasi puting beliung.")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption(
    "© Sistem Deteksi Dini Puting Beliung | "
    "BMKG-style Operational Dashboard"
)
