# ==========================================================
#  PLOTTER – PETA REALTIME PUTING BELIUNG (POLYGON RISIKO)
#  Module : visualization/plotter.py
# ==========================================================

import folium
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

# ======================
# COLOR MAP LEVEL
# ======================
LEVEL_COLOR = {
    "WASPADA": "#FFF176",  # kuning
    "SIAGA": "#FFB74D",    # oranye
    "AWAS": "#E57373"      # merah
}

# ======================
# LOAD BATAS WILAYAH
# ======================
@st.cache_data
def load_boundary():
    """
    GeoJSON wilayah (prov/kab/kec/desa)
    HARUS punya kolom 'wilayah'
    """
    return gpd.read_file("data/shp/batas_wilayah.geojson")

# ======================
# HITUNG LEVEL PER WILAYAH
# ======================
def aggregate_level(realtime_df):
    """
    Ambil level tertinggi per wilayah
    """
    if realtime_df is None or realtime_df.empty:
        return {}

    priority = {"WASPADA": 1, "SIAGA": 2, "AWAS": 3}

    agg = {}
    for _, row in realtime_df.iterrows():
        w = row["wilayah"]
        lvl = row["level"]

        if w not in agg or priority[lvl] > priority[agg[w]]:
            agg[w] = lvl

    return agg

# ======================
# RENDER MAP
# ======================
def render_realtime_map(realtime_df, height=600):

    m = folium.Map(
        location=[-7.5, 112.5],
        zoom_start=8,
        tiles="CartoDB positron"
    )

    # ------------------
    # POLYGON RISIKO
    # ------------------
    try:
        gdf = load_boundary()
        level_map = aggregate_level(realtime_df)

        def style_func(feature):
            wilayah = feature["properties"].get("wilayah")
            level = level_map.get(wilayah)

            return {
                "fillColor": LEVEL_COLOR.get(level, "transparent"),
                "color": "#444444",
                "weight": 1,
                "fillOpacity": 0.6 if level else 0.1
            }

        folium.GeoJson(
            gdf,
            name="Risiko Puting Beliung",
            style_function=style_func,
            tooltip=folium.GeoJsonTooltip(
                fields=["wilayah"],
                aliases=["Wilayah"]
            )
        ).add_to(m)

    except Exception as e:
        st.warning(f"Gagal memuat polygon wilayah: {e}")

    # ------------------
    # TITIK DETAIL
    # ------------------
    if realtime_df is not None and not realtime_df.empty:
        for _, row in realtime_df.iterrows():
            color = LEVEL_COLOR.get(row["level"], "blue")

            popup = f"""
            <b>Wilayah</b>: {row['wilayah']}<br>
            <b>Level</b>: {row['level']}<br>
            <b>Detail</b>: {row['keterangan']}
            """

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=7,
                color=color,
                fill=True,
                fill_opacity=0.9,
                popup=popup
            ).add_to(m)

    folium.LayerControl().add_to(m)

    st_folium(m, width=1200, height=height)
