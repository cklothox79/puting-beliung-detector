# ==========================================================
#  REPORT GENERATOR – PDF BMKG STYLE
#  Module : engine/report.py
# ==========================================================

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime
import os

# ======================
# GENERATE PDF
# ======================
def generate_pdf_report(df, narrative, output_dir="reports"):
    """
    Membuat laporan PDF operasional BMKG
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    filename = f"Laporan_Puting_Beliung_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    y = height - 2 * cm

    # ======================
    # HEADER
    # ======================
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(
        width / 2,
        y,
        "LAPORAN PEMANTAUAN DINI PUTING BELIUNG"
    )

    y -= 1 * cm

    c.setFont("Helvetica", 10)
    c.drawCentredString(
        width / 2,
        y,
        "Berdasarkan Analisis Dinamika Atmosfer dan Data Satelit"
    )

    y -= 1.2 * cm

    # ======================
    # WAKTU
    # ======================
    c.setFont("Helvetica", 9)
    waktu = datetime.utcnow().strftime("%d %B %Y, %H:%M UTC")
    c.drawString(2 * cm, y, f"Waktu Analisis : {waktu}")

    y -= 1 * cm

    # ======================
    # NARASI
    # ======================
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, y, "Ringkasan Kondisi:")

    y -= 0.6 * cm

    c.setFont("Helvetica", 9)
    text = c.beginText(2 * cm, y)
    for line in narrative.split(". "):
        text.textLine(line.strip())
    c.drawText(text)

    y -= 3 * cm

    # ======================
    # TABEL DATA
    # ======================
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, y, "Titik Wilayah Terindikasi:")

    y -= 0.6 * cm
    c.setFont("Helvetica", 9)

    if df is not None and not df.empty:
        for _, row in df.iterrows():
            line = (
                f"- {row['wilayah']} | "
                f"Level: {row['level']} | "
                f"Shear: {row.get('shear','-')} kt | "
                f"CAPE: {row.get('cape','-')} J/kg"
            )
            c.drawString(2.2 * cm, y, line)
            y -= 0.45 * cm

            if y < 2 * cm:
                c.showPage()
                y = height - 2 * cm
                c.setFont("Helvetica", 9)
    else:
        c.drawString(2.2 * cm, y, "- Tidak terdapat indikasi signifikan.")

    # ======================
    # FOOTER
    # ======================
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(
        width / 2,
        1.5 * cm,
        "Sistem Deteksi Dini Puting Beliung – Operasional"
    )

    c.save()
    return filepath
