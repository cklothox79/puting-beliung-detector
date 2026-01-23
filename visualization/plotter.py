# ==========================================================
#  PLOTTER – PETA REALTIME PUTING BELIUNG
#  Module : visualization/plotter.py
# ==========================================================

import folium
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

# ======================
# LOAD SHAPEFILE (CACHE)
# ======================
@st.cache_data
def load_boundary():
    """
    Load batas wilayah (GeoJSON).
    Disarankan: kecamatan / desa dalam format GeoJSON.
    """
    return gpd.read_file("data/shp/batas_wilayah.geojson")


# ======================
# RENDER MAP
# ======================
def render_realtime_map(realtime_df, height=600):
    """
    Menampilkan peta realtime dengan overlay wilayah
    dan titik indikasi puting beliung
    """

    # ------------------
    # Base Map
    # ------------------
    m = folium.Map(
        location=[-7.5, 112.5],  # Jawa Timur
        zoom_start=8,
        tiles="CartoDB positron"
    )

    # ------------------
    # Overlay Wilayah
    # ------------------
    try:
        gdf = load_boundary()

        folium.GeoJson(
            gdf,
            name="Batas Wilayah",
            style_function=lambda x: {
                "fillColor": "transparent",
                "color": "#333333",
                "weight": 1
            },
            tooltip=folium.GeoJsonTooltip(
                fields=[gdf.columns[0]],
                aliases=["Wilayah"]
            )
        ).add_to(m)

    except Exception as e:
        st.warning(f"Gagal memuat batas wilayah: {e}")

    # ------------------
    # Titik Realtime
    # ------------------
    if realtime_df is not None and not realtime_df.empty:
        for _, row in realtime_df.iterrows():

            # Tentukan warna berdasar level
            level = row.get("level", "WASPADA")

            if level == "AWAS":
                color = "red"
            elif level == "SIAGA":
                color = "orange"
            else:
                color = "yellow"

            popup_text = f"""
            <b>Lokasi</b> : {row.get('wilayah','-')}<br>
            <b>Level</b> : {level}<br>
            <b>Keterangan</b> : {row.get('keterangan','-')}
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=7,
                color=color,
                fill=True,
                fill_opacity=0.85,
                popup=popup_text
            ).add_to(m)

    folium.LayerControl().add_to(m)

    # ------------------
    # Render ke Streamlit
    # ------------------
    st_folium(
        m,
        width=1200,
        height=height
    )
