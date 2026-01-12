# ==========================================================
# plotter.py
# Visualisasi Peta Risiko Puting Beliung
# Versi: BMKG Operasional
# ==========================================================

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime

# ==========================================================
# PETA GRID RISIKO
# ==========================================================
def plot_risk_map(ds, region_name="Wilayah Kajian", save_path=None):
    """
    Plot peta risiko puting beliung (grid)
    """
    if "RISK_FLAG_FILTERED" not in ds:
        raise ValueError("Jalankan detector terlebih dahulu")

    risk = ds["RISK_FLAG_FILTERED"].isel(time=-1)

    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Extent otomatis
    ax.set_extent(
        [
            float(risk.lon.min()),
            float(risk.lon.max()),
            float(risk.lat.min()),
            float(risk.lat.max()),
        ],
        crs=ccrs.PlateCarree(),
    )

    # Base map
    ax.add_feature(cfeature.COASTLINE, linewidth=1)
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAND, alpha=0.4)
    ax.add_feature(cfeature.OCEAN, alpha=0.3)

    # Plot risiko
    mesh = ax.pcolormesh(
        risk.lon,
        risk.lat,
        risk,
        transform=ccrs.PlateCarree(),
    )

    # Colorbar manual
    cbar = plt.colorbar(mesh, ax=ax, shrink=0.7)
    cbar.set_ticks([0, 1, 2])
    cbar.set_ticklabels(["Normal", "Waspada", "Bahaya"])
    cbar.set_label("Tingkat Risiko")

    # Judul
    waktu = datetime.utcnow().strftime("%d %B %Y %H:%M UTC")
    ax.set_title(
        f"PETA RISIKO PUTING BELIUNG\n{region_name}\n{waktu}",
        fontsize=12,
        weight="bold",
    )

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")

    plt.show()
