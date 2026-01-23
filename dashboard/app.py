# ==========================================================
#  PUTING BELIUNG DETECTOR – DASHBOARD OPERASIONAL
#  MODE PUBLIK & INTERNAL
# ==========================================================

import streamlit as st

from engine.realtime import load_realtime_data
from engine.narrator import generate_narrative
from engine.report import generate_pdf_report
from engine.logger import setup_logger

from visualization.plotter import render_realtime_map

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Puting Beliung Detector",
    page_icon="🌪️",
    layout="wide"
)

logger = setup_logger()

# ======================
# SIDEBAR – MODE AKSES
# ======================
st.sidebar.title("🌪️ Puting Beliung Detector")
st.sidebar.caption("Dashboard Operasional")

st.sidebar.markdown("## 🔐 Mode Akses")

MODE_INTERNAL_PASSWORD = "bmkg_internal"  # ganti sesuai kebutuhan

mode = st.sidebar.radio(
    "Pilih Mode",
    ["Publik", "Internal"],
    index=0
)

is_internal = False
if mode == "Internal":
    pwd = st.sidebar.text_input("Password Internal", type="password")
    if pwd == MODE_INTERNAL_PASSWORD:
        is_internal = True
        st.sidebar.success("Akses Internal Aktif")
    else:
        st.sidebar.warning("Masukkan password internal")

# ======================
# SIDEBAR – REFRESH
# ======================
st.sidebar.markdown("---")
interval = st.sidebar.selectbox(
    "⏱️ Interval Update (detik)",
    [30, 60, 120, 300],
    index=1
)

st.experimental_autorefresh(
    interval=interval * 1000,
    key="auto_refresh_dashboard"
)

# ======================
# HEADER UTAMA
# ======================
st.title("🌪️ Dashboard Realtime Deteksi Puting Beliung")

st.markdown(
    """
    Sistem pemantauan dini berbasis analisis dinamika atmosfer  
    dan pengolahan data satelit secara realtime.
    """
)

# ======================
# LOAD DATA REALTIME
# ======================
try:
    df_realtime = load_realtime_data()
    logger.info("Realtime data loaded")
except Exception as e:
    st.error("Gagal memuat data realtime")
    logger.error(f"Realtime load error: {e}")
    df_realtime = None

# ======================
# PETA REALTIME (PUBLIK & INTERNAL)
# ======================
st.subheader("🗺️ Peta Realtime Wilayah Terindikasi")

render_realtime_map(
    realtime_df=df_realtime,
    height=600,
    internal=is_internal
)

# ======================
# KONTEN INTERNAL SAJA
# ======================
if is_internal:

    st.subheader("📋 Data Realtime Deteksi")
    if df_realtime is not None and not df_realtime.empty:
        st.dataframe(df_realtime, use_container_width=True)
    else:
        st.info("Belum terdapat indikasi signifikan.")

    st.subheader("📝 Narasi Operasional BMKG")
    narasi = generate_narrative(df_realtime)
    st.info(narasi)

    # ======================
    # EXPORT PDF
    # ======================
    st.sidebar.markdown("---")
    if st.sidebar.button("📄 Export PDF Laporan"):
        pdf_path = generate_pdf_report(
            df_realtime,
            narasi
        )
        st.sidebar.success("Laporan berhasil dibuat")
        st.sidebar.download_button(
            "⬇️ Download PDF",
            open(pdf_path, "rb"),
            file_name=pdf_path.split("/")[-1]
        )

else:
    st.caption(
        "ℹ️ Detail teknis, narasi analisis, dan laporan PDF "
        "hanya tersedia pada mode internal."
    )

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption(
    "© Sistem Deteksi Dini Puting Beliung | Dashboard Operasional"
)
