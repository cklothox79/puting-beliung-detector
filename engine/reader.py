# ==========================================================
# reader.py
# Engine Pembaca Data Puting Beliung
# Versi: BMKG-style | Offline → Realtime-ready
# ==========================================================

import os
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import xarray as xr
import yaml

# ==========================================================
# PATH DASAR
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"

# ==========================================================
# UTIL DASAR
# ==========================================================
def load_config(file_name: str):
    """Load file YAML konfigurasi"""
    path = CONFIG_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"Config tidak ditemukan: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_time(dt, tz="UTC"):
    """
    Normalisasi waktu ke format datetime (UTC default)
    """
    if isinstance(dt, str):
        dt = pd.to_datetime(dt)
    if tz.upper() == "WIB":
        dt = dt - timedelta(hours=7)
    return dt


# ==========================================================
# 1️⃣ READER DATA CONTOH (MOCK / DEV)
# ==========================================================
def read_sample_data():
    """
    Data contoh untuk pengembangan awal
    Output: xarray.Dataset
    """
    time = pd.date_range("2026-01-01 00:00", periods=6, freq="10min")
    lat = np.linspace(-8.5, -7.0, 20)
    lon = np.linspace(112.0, 113.5, 20)

    bt = 290 - 40 * np.random.rand(len(time), len(lat), len(lon))
    rcr = -5 * np.random.rand(len(time), len(lat), len(lon))

    ds = xr.Dataset(
        {
            "BT_IR": (("time", "lat", "lon"), bt),
            "RCR": (("time", "lat", "lon"), rcr),
        },
        coords={
            "time": time,
            "lat": lat,
            "lon": lon,
        },
        attrs={
            "source": "MOCK DATA",
            "description": "Sample Himawari-like dataset",
        },
    )
    return ds


# ==========================================================
# 2️⃣ READER DATA SATELIT (HIMAWARI STYLE)
# ==========================================================
def read_satellite_nc(file_path: str):
    """
    Membaca data satelit NetCDF/HDF
    Output: xarray.Dataset
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File satelit tidak ditemukan: {file_path}")

    ds = xr.open_dataset(file_path)

    # Standarisasi nama koordinat
    rename_map = {}
    if "latitude" in ds.coords:
        rename_map["latitude"] = "lat"
    if "longitude" in ds.coords:
        rename_map["longitude"] = "lon"

    if rename_map:
        ds = ds.rename(rename_map)

    # Pastikan time ada
    if "time" not in ds.coords:
        raise ValueError("Dataset satelit tidak memiliki koordinat time")

    ds.attrs["reader"] = "BMKG Satellite Reader"
    return ds


# ==========================================================
# 3️⃣ READER DATA NWP (ERA5 / WRF / GSM)
# ==========================================================
def read_nwp_nc(file_path: str, level=None):
    """
    Membaca data NWP (NetCDF)
    level: tekanan (hPa), misal 850, 700, 500
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File NWP tidak ditemukan: {file_path}")

    ds = xr.open_dataset(file_path)

    if level and "level" in ds.dims:
        ds = ds.sel(level=level)

    ds.attrs["reader"] = "BMKG NWP Reader"
    return ds


# ==========================================================
# 4️⃣ READER DATA OBSERVASI (CSV / AWS)
# ==========================================================
def read_observation_csv(file_path: str):
    """
    Membaca data observasi permukaan (AWS / Pos Hujan)
    Output: pandas.DataFrame
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File observasi tidak ditemukan: {file_path}")

    df = pd.read_csv(file_path)

    # Standarisasi kolom waktu
    time_cols = ["time", "datetime", "tanggal"]
    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
            df = df.rename(columns={col: "time"})
            break

    if "time" not in df.columns:
        raise ValueError("Kolom waktu tidak ditemukan pada data observasi")

    return df


# ==========================================================
# 5️⃣ SUBSET DATA PER KECAMATAN
# ==========================================================
def subset_by_region(ds, lat_min, lat_max, lon_min, lon_max):
    """
    Potong dataset berdasarkan bounding box wilayah
    """
    return ds.sel(
        lat=slice(lat_min, lat_max),
        lon=slice(lon_min, lon_max),
    )


# ==========================================================
# 6️⃣ PIPELINE READER TERPADU
# ==========================================================
def load_event_data(
    sat_file=None,
    nwp_file=None,
    obs_file=None,
    region_bbox=None,
):
    """
    Pipeline pembaca data kejadian cuaca ekstrem
    """
    data = {}

    if sat_file:
        data["satellite"] = read_satellite_nc(sat_file)

    if nwp_file:
        data["nwp"] = read_nwp_nc(nwp_file)

    if obs_file:
        data["observation"] = read_observation_csv(obs_file)

    # Subset wilayah
    if region_bbox:
        lat_min, lat_max, lon_min, lon_max = region_bbox
        for key, ds in data.items():
            if isinstance(ds, xr.Dataset):
                data[key] = subset_by_region(
                    ds, lat_min, lat_max, lon_min, lon_max
                )

    return data


# ==========================================================
# MAIN TEST (DEV MODE)
# ==========================================================
if __name__ == "__main__":
    print("🔍 Testing reader.py (BMKG version)")
    ds = read_sample_data()
    print(ds)
