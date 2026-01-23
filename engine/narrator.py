# ==========================================================
#  NARRATOR – NARASI OTOMATIS BMKG
#  Module : engine/narrator.py
# ==========================================================

from datetime import datetime

# ======================
# TEMPLATE KALIMAT
# ======================
LEVEL_TEXT = {
    "WASPADA": "perlu diwaspadai potensi cuaca ekstrem skala lokal",
    "SIAGA": "terdapat peningkatan potensi kejadian cuaca ekstrem",
    "AWAS": "berpotensi terjadi cuaca ekstrem signifikan berupa puting beliung"
}

# ======================
# GENERATE NARASI
# ======================
def generate_narrative(df):
    """
    Membuat narasi operasional BMKG
    input: DataFrame hasil detector
    """

    if df is None or df.empty:
        return (
            "Berdasarkan hasil pemantauan dinamika atmosfer dan citra satelit, "
            "tidak terpantau adanya indikasi signifikan potensi puting beliung "
            "di wilayah Jawa Timur pada periode pengamatan."
        )

    waktu = datetime.utcnow().strftime("%d %B %Y pukul %H:%M UTC")

    wilayah_list = df["wilayah"].unique().tolist()
    wilayah_text = ", ".join(wilayah_list)

    level_tertinggi = df["level"].value_counts().idxmax()

    narasi = (
        f"Berdasarkan hasil analisis dinamika atmosfer dan pengolahan data satelit, "
        f"terpantau {LEVEL_TEXT[level_tertinggi]} "
        f"di wilayah {wilayah_text} "
        f"pada {waktu}. "
    )

    # Detail teknis (opsional tapi BMKG banget)
    narasi += (
        "Kondisi ini didukung oleh adanya labilitas atmosfer sedang hingga kuat "
        "yang ditandai dengan nilai CAPE yang cukup tinggi, "
        "serta dukungan faktor dinamika atmosfer berupa shear angin rendah "
        "dan pertumbuhan awan konvektif signifikan. "
    )

    narasi += (
        "Masyarakat diimbau untuk tetap waspada terhadap potensi "
        "angin kencang sesaat, hujan lebat, dan fenomena cuaca ekstrem lainnya."
    )

    return narasi
