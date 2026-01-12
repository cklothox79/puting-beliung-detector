# ==========================================================
# preprocessor.py
# QC & Preprocessing Data Puting Beliung
# Versi: BMKG Operasional
# ==========================================================

import numpy as np
import xarray as xr

# ==========================================================
# 1️⃣ QUALITY CONTROL DASAR
# ==========================================================
def qc_range(ds, var_name, vmin=None, vmax=None):
    """
    QC berbasis batas fisik
    """
    if var_name not in ds:
        raise ValueError(f"Variabel {var_name} tidak ditemukan")

    da = ds[var_name]

    if vmin is not None:
        da = da.where(da >= vmin)
    if vmax is not None:
        da = da.where(da <= vmax)

    ds[var_name] = da
    return ds


# ==========================================================
# 2️⃣ FILL MISSING VALUE
# ==========================================================
def fill_missing(ds, method="linear"):
    """
    Mengisi data hilang (time-based)
    """
    for var in ds.data_vars:
        if "time" in ds[var].dims:
            ds[var] = ds[var].interpolate_na(
                dim="time", method=method, fill_value="extrapolate"
            )
    return ds


# ==========================================================
# 3️⃣ TEMPORAL SMOOTHING
# ==========================================================
def smooth_time(ds, window=3):
    """
    Smoothing temporal (rolling mean)
    window: jumlah timestep
    """
    for var in ds.data_vars:
        if "time" in ds[var].dims:
            ds[var] = ds[var].rolling(
                time=window, center=True, min_periods=1
            ).mean()
    return ds


# ==========================================================
# 4️⃣ STANDARISASI DATA SATELIT
# ==========================================================
def preprocess_satellite(ds):
    """
    Pipeline preprocessing data satelit
    """
    # QC Brightness Temperature IR
    if "BT_IR" in ds:
        ds = qc_range(ds, "BT_IR", vmin=180, vmax=330)

    # QC Rapid Cooling Rate
    if "RCR" in ds:
        ds = qc_range(ds, "RCR", vmin=-20, vmax=5)

    ds = fill_missing(ds)
    ds = smooth_time(ds, window=3)

    ds.attrs["preprocess"] = "BMKG Satellite Preprocessing"
    return ds


# ==========================================================
# 5️⃣ STANDARISASI DATA NWP
# ==========================================================
def preprocess_nwp(ds):
    """
    Preprocessing NWP (RH, angin, dsb)
    """
    # RH harus 0-100%
    for var in ds.data_vars:
        if "rh" in var.lower():
            ds = qc_range(ds, var, vmin=0, vmax=100)

    ds = fill_missing(ds)
    ds = smooth_time(ds, window=3)

    ds.attrs["preprocess"] = "BMKG NWP Preprocessing"
    return ds


# ==========================================================
# 6️⃣ PIPELINE TERPADU
# ==========================================================
def preprocess_all(data_dict):
    """
    data_dict dari reader.load_event_data()
    """
    output = {}

    for key, data in data_dict.items():
        if isinstance(data, xr.Dataset):
            if key == "satellite":
                output[key] = preprocess_satellite(data)
            elif key == "nwp":
                output[key] = preprocess_nwp(data)
            else:
                output[key] = data
        else:
            output[key] = data

    return output


# ==========================================================
# MAIN TEST
# ==========================================================
if __name__ == "__main__":
    print("🧪 Test preprocessor BMKG")
