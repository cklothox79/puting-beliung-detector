# ==========================================================
# narrator.py
# Narasi Otomatis Puting Beliung
# Versi: BMKG Operasional
# ==========================================================

from datetime import datetime
import pandas as pd

# ==========================================================
# UTIL FORMAT WAKTU
# ==========================================================
def format_time(dt):
    """
    Format waktu gaya BMKG
    """
    if isinstance(dt, str):
        dt = pd.to_datetime(dt)
    return dt.strftime("%d %B %Y pukul %H.%M WIB")


# ==========================================================
# 1️⃣ NARASI STATUS UMUM
# ==========================================================
def general_narrative(decision_df, region_name="wilayah kajian"):
    """
    Narasi status umum cuaca ekstrem
    """
    latest = decision_df.iloc[-1]

    status = latest["status"]
    waktu = format_time(latest["time"])

    narasi = (
        f"Berdasarkan hasil analisis dinamika atmosfer dan pemantauan "
        f"citra satelit terkini, kondisi cuaca di {region_name} pada "
        f"{waktu} berada pada status **{status}**."
    )

    return narasi


# ==========================================================
# 2️⃣ NARASI DINAMIKA ATMOSFER
# ==========================================================
def dynamic_narrative(ds):
    """
    Narasi berbasis parameter fisis
    """
    kalimat = []

    if "BT_IR" in ds:
        bt_min = float(ds["BT_IR"].min())
        kalimat.append(
            f"Suhu puncak awan teramati relatif dingin dengan nilai minimum "
            f"sekitar {bt_min:.1f} K, mengindikasikan pertumbuhan awan "
            f"konvektif signifikan."
        )

    if "RCR" in ds:
        rcr_max = float(ds["RCR"].max())
        kalimat.append(
            f"Terdapat indikasi pendinginan cepat puncak awan "
            f"dengan nilai Rapid Cooling Rate mencapai "
            f"{rcr_max:.1f} K per 10 menit."
        )

    if "CI" in ds:
        ci_max = float(ds["CI"].max())
        kalimat.append(
            f"Indeks komposit konvektif menunjukkan nilai maksimum "
            f"hingga {ci_max:.2f}, yang mencerminkan peningkatan potensi "
            f"cuaca ekstrem."
        )

    return " ".join(kalimat)


# ==========================================================
# 3️⃣ NARASI DAMPAK POTENSIAL
# ==========================================================
def impact_narrative(status):
    """
    Narasi dampak cuaca ekstrem
    """
    if "PERINGATAN" in status:
        return (
            "Kondisi tersebut berpotensi menimbulkan kejadian puting beliung, "
            "angin kencang, hujan lebat disertai kilat/petir, serta berisiko "
            "menyebabkan kerusakan infrastruktur ringan hingga sedang."
        )
    elif "WASPADA" in status:
        return (
            "Masyarakat diimbau untuk tetap waspada terhadap kemungkinan "
            "terjadinya cuaca ekstrem berskala lokal."
        )
    else:
        return (
            "Secara umum kondisi atmosfer relatif stabil dan belum "
            "menunjukkan potensi signifikan cuaca ekstrem."
        )


# ==========================================================
# 4️⃣ NARASI REKOMENDASI
# ==========================================================
def recommendation_narrative(status):
    """
    Rekomendasi tindak lanjut
    """
    if "PERINGATAN" in status:
        return (
            "Disarankan kepada instansi terkait dan masyarakat "
            "untuk meningkatkan kewaspadaan serta melakukan langkah "
            "antisipasi terhadap potensi dampak cuaca ekstrem."
        )
    elif "WASPADA" in status:
        return (
            "Disarankan untuk terus memantau informasi cuaca terkini "
            "dari BMKG."
        )
    else:
        return (
            "Pemantauan kondisi cuaca akan terus dilakukan secara rutin."
        )


# ==========================================================
# 5️⃣ PIPELINE NARASI TERPADU
# ==========================================================
def generate_full_narrative(
    detection_output,
    region_name="wilayah kajian"
):
    """
    Menghasilkan narasi lengkap BMKG-style
    """
    decision_df = detection_output["decision"]
    ds = detection_output["dataset"]

    latest_status = decision_df.iloc[-1]["status"]

    narasi = []
    narasi.append(general_narrative(decision_df, region_name))
    narasi.append(dynamic_narrative(ds))
    narasi.append(impact_narrative(latest_status))
    narasi.append(recommendation_narrative(latest_status))

    return "\n\n".join(narasi)


# ==========================================================
# MAIN TEST
# ==========================================================
if __name__ == "__main__":
    print("🗣️ Narrator BMKG siap digunakan")
