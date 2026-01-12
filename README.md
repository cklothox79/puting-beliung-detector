# 🌪️ Puting Beliung Detector
### Early Detection Engine berbasis Satelit, NWP, dan Observasi
🛰️ Operasional • 🔬 Ilmiah • ⚡ Realtime-ready

---

## 📌 Deskripsi
**Puting Beliung Detector** adalah sistem deteksi dini potensi
kejadian puting beliung berbasis:

- Satelit (Himawari-8/9)
- Parameter dinamika atmosfer
- Indeks konvektif (Rapid Cooling Rate, Composite Index, dll)

Dirancang untuk:
- Analisis pascakejadian
- Peringatan dini skala kecamatan
- Narasi otomatis untuk briefing BMKG

---

## 🎯 Tujuan
- Mendeteksi sinyal awal awan konvektif berbahaya
- Memberikan **skor potensi puting beliung**
- Menghasilkan **narasi analisis cuaca otomatis**
- Modular & siap dikembangkan ke **realtime system**

---

## 🧠 Arsitektur Sistem

```text
DATA → reader → preprocessing → indices → detector → narasi → visual
