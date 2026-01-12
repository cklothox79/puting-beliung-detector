# ==========================================================
# indices.py
# Perhitungan Indeks Puting Beliung
# Versi: BMKG Operasional
# ==========================================================

import numpy as np
import xarray as xr

# ==========================================================
# 1️⃣ RAPID COOLING RATE (RCR)
# ==========================================================
def compute_rcr(ds, bt_var="BT_IR"):
    """
    Menghitung Rapid Cooling Rate (K/10 menit)
    RCR = dT/dt
    """
    if bt_var not in ds:
        raise ValueError(f"{bt_var} tidak ditemukan")

    bt = ds[bt_var]

    # turunan waktu
    rcr = bt.diff(dim="time") * -1

    rcr = rcr.assign_coords(
        time=bt.time[1:]
    )

    rcr.name = "RCR"
    rcr.attrs["unit"] = "K/10min"
    rcr.attrs["description"] = "Rapid Cooling Rate"

    return rcr


# ==========================================================
# 2️⃣ INDIKATOR AWAN KONVEKTIF
# ==========================================================
def convective_indicator(ds):
    """
    Indikator sederhana awan konvektif
    """
    indicators = {}

    if "BT_IR" in ds:
        indicators["deep_convection"] = ds["BT_IR"] < 235

    if "RCR" in ds:
        indicators["rapid_growth"] = ds["RCR"] > 3

    return indicators


# ==========================================================
# 3️⃣ COMPOSITE INDEX (CI)
# ==========================================================
def composite_index(ds):
    """
    Composite Index Puting Beliung
    Skala 0 - 1
    """
    score = xr.zeros_like(ds["BT_IR"])

    # Faktor 1: BT dingin
    score = score + xr.where(ds["BT_IR"] < 235, 0.4, 0)

    # Faktor 2: pendinginan cepat
    if "RCR" in ds:
        score = score + xr.where(ds["RCR"] > 3, 0.4, 0)

    # Faktor 3: awan sangat dingin
    score = score + xr.where(ds["BT_IR"] < 220, 0.2, 0)

    score = score.clip(0, 1)
    score.name = "CI"

    score.attrs["description"] = "Composite Index Puting Beliung"
    score.attrs["scale"] = "0 (rendah) - 1 (tinggi)"

    return score


# ==========================================================
# 4️⃣ PIPELINE HITUNG INDEKS
# ==========================================================
def calculate_indices(ds):
    """
    Pipeline perhitungan indeks
    """
    output = ds.copy()

    # Hitung RCR jika belum ada
    if "RCR" not in output and "BT_IR" in output:
        rcr = compute_rcr(output)
        output["RCR"] = rcr

    # Hitung Composite Index
    ci = composite_index(output)
    output["CI"] = ci

    output.attrs["indices"] = "BMKG Convective Indices"
    return output


# ==========================================================
# 5️⃣ KLASIFIKASI LEVEL RISIKO
# ==========================================================
def classify_risk(ci):
    """
    Klasifikasi risiko berdasarkan CI
    """
    return xr.where(
        ci >= 0.7, "TINGGI",
        xr.where(ci >= 0.4, "SEDANG", "RENDAH")
    )


# ==========================================================
# MAIN TEST
# ==========================================================
if __name__ == "__main__":
    print("🧪 Test indices BMKG")
