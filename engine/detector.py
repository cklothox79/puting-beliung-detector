# ==========================================================
# detector.py
# Engine Keputusan Puting Beliung
# Versi: BMKG Operasional
# ==========================================================

import numpy as np
import xarray as xr
import pandas as pd

# ==========================================================
# PARAMETER DEFAULT (bisa dipindah ke config.yaml)
# ==========================================================
CI_HIGH = 0.7
CI_MED = 0.4
RCR_THRESHOLD = 3.0
BT_DEEP = 235
BT_VERY_DEEP = 220


# ==========================================================
# 1️⃣ DETEKSI GRID BERISIKO
# ==========================================================
def detect_grid_risk(ds):
    """
    Deteksi grid berpotensi puting beliung
    Output: Dataset + flag risiko
    """
    if "CI" not in ds:
        raise ValueError("CI belum tersedia, jalankan indices.py dulu")

    risk_flag = xr.zeros_like(ds["CI"], dtype=int)

    # Skema logika BMKG
    risk_flag = xr.where(ds["CI"] >= CI_HIGH, 2, risk_flag)
    risk_flag = xr.where(
        (ds["CI"] >= CI_MED) &
        (ds["RCR"] >= RCR_THRESHOLD) &
        (ds["BT_IR"] <= BT_DEEP),
        1,
        risk_flag
    )

    risk_flag.name = "RISK_FLAG"
    risk_flag.attrs["description"] = "0: rendah | 1: waspada | 2: bahaya"

    ds["RISK_FLAG"] = risk_flag
    return ds


# ==========================================================
# 2️⃣ FILTER KONSISTENSI WAKTU
# ==========================================================
def temporal_consistency(ds, min_duration=2):
    """
    Menyaring sinyal sesaat (noise)
    min_duration: jumlah timestep berturut-turut
    """
    flag = ds["RISK_FLAG"]

    def _filter(series):
        count = 0
        out = []
        for v in series:
            if v > 0:
                count += 1
            else:
                count = 0
            out.append(v if count >= min_duration else 0)
        return np.array(out)

    filtered = xr.apply_ufunc(
        _filter,
        flag,
        input_core_dims=[["time"]],
        output_core_dims=[["time"]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[int],
    )

    filtered.name = "RISK_FLAG_FILTERED"
    filtered.attrs["description"] = "Risiko setelah filter temporal"

    ds["RISK_FLAG_FILTERED"] = filtered
    return ds


# ==========================================================
# 3️⃣ AGREGASI WILAYAH (KECAMATAN)
# ==========================================================
def aggregate_region(ds, method="max"):
    """
    Agregasi risiko wilayah
    """
    flag = ds["RISK_FLAG_FILTERED"]

    if method == "max":
        region_risk = flag.max(dim=["lat", "lon"])
    elif method == "mean":
        region_risk = flag.mean(dim=["lat", "lon"])
    else:
        raise ValueError("Metode agregasi tidak dikenal")

    region_risk.name = "REGION_RISK"
    region_risk.attrs["description"] = "Risiko agregat wilayah"

    return region_risk


# ==========================================================
# 4️⃣ KEPUTUSAN OPERASIONAL
# ==========================================================
def decision_engine(region_risk):
    """
    Mengubah angka menjadi keputusan
    """
    decisions = []

    for t, val in zip(region_risk.time.values, region_risk.values):
        if val >= 2:
            status = "PERINGATAN DINI PUTING BELIUNG"
        elif val >= 1:
            status = "WASPADA CUACA EKSTREM"
        else:
            status = "NORMAL"

        decisions.append({
            "time": pd.to_datetime(t),
            "risk_value": float(val),
            "status": status
        })

    return pd.DataFrame(decisions)


# ==========================================================
# 5️⃣ PIPELINE DETEKSI TERPADU
# ==========================================================
def run_detection(ds):
    """
    Pipeline lengkap deteksi puting beliung
    """
    ds = detect_grid_risk(ds)
    ds = temporal_consistency(ds)
    region_risk = aggregate_region(ds)
    decision = decision_engine(region_risk)

    return {
        "dataset": ds,
        "region_risk": region_risk,
        "decision": decision
    }


# ==========================================================
# MAIN TEST
# ==========================================================
if __name__ == "__main__":
    print("⚠️ Detector BMKG siap dijalankan")
