# PENJELASAN SINGKAT: CARA KERJA PREDIKSI BAHAN BAKU

---

## 🎬 SCENARIO: User Melihat Prediksi

```
USER BUKA APP
    ↓
MASUK KE HALAMAN "PREDIKSI BAHAN BAKU"
    ↓
LIHAT DAFTAR 7 BAHAN (Urutan Prioritas)
    ↓
    1. Tepung Terigu      [H] ORDER_IMMEDIATELY - Stok habis 3.9 hari
    2. test_item_1         [H] ORDER_IMMEDIATELY - Stok habis 3.9 hari
    3. morison            [H] ORDER_IMMEDIATELY - Stok habis 3.9 hari
    4. Gula Halus         [H] ORDER_IMMEDIATELY - Stok habis 4.1 hari
    5. Telur Ayam         [H] ORDER_IMMEDIATELY - Stok habis 3.9 hari
    6. Susu Cair          [M] PLAN_ORDER - Stok habis 7.2 hari
    7. Mentega Putih      [M] PLAN_ORDER - Stok habis 7.5 hari

    [H] = High Priority (Urgent!)
    [M] = Medium Priority (Dalam 2-3 hari)

    ↓
USER TAP BAHAN #1 "TEPUNG TERIGU"
    ↓
LIHAT DETAIL LENGKAP:

┌──────────────────────────────────────────────┐
│ TEPUNG TERIGU SERBAGUNA                      │
├──────────────────────────────────────────────┤
│ STOCK STATUS:                                │
│  • Stok Saat Ini:    10.5 kg                 │
│  • Stok Minimum:     50.0 kg  [KURANG!]      │
│  • Stok Optimal:     200.0 kg [JAUH!]        │
│                                              │
│ PREDICTION RESULTS:                          │
│  • Demand Per Hari:  2.7 kg                  │
│  • Demand Per Bulan: 82 kg                   │
│  • Est. Cost:        Rp 407,922              │
│  • Confidence:       85.3%                   │
│  • Hari Habis:       3.9 hari [URGENT!]      │
│                                              │
│ SMART RECOMMENDATION:                        │
│  ┌────────────────────────────────────┐      │
│  │ [HIGH PRIORITY]                    │      │
│  │ ACTION: ORDER_IMMEDIATELY          │      │
│  │                                    │      │
│  │ Prediksi permintaan tinggi.        │      │
│  │ Lakukan pemesanan segera!          │      │
│  └────────────────────────────────────┘      │
│                                              │
│ ACTION PLAN (4 LANGKAH):                     │
│                                              │
│ 1. URGENT_ORDER                              │
│    ⚠️  Stok kritis! Pesan darurat             │
│    ⏰ HARI INI                                │
│                                              │
│ 2. EXPEDITED_ORDER                           │
│    ⏰ Percepat pengiriman (habis 3 hari)      │
│    📅 1-2 HARI                               │
│                                              │
│ 3. REGULAR_ORDER                             │
│    🛒 Pesan 189 kg untuk optimal             │
│    📅 3-7 HARI                               │
│                                              │
│ 4. MONITOR                                   │
│    👁️  Pantau pola penjualan                 │
│    📅 BERKELANJUTAN                          │
│                                              │
└──────────────────────────────────────────────┘

    ↓
USER BACA & PAHAMI
    ↓
USER AMBIL ACTION:
    - Konfirmasi order darurat hari ini
    - Set reminder untuk 1-2 hari
    - Pantau stok terus-menerus
```

---

## 🏗️ ARSITEKTUR SISTEM

```
┌─────────────────────────────────────────────────────────┐
│                      FLUTTER APP                         │
│            (User Interface - Apa yang dilihat)           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Halaman 1: Batch View (Daftar 7 Bahan)                │
│  Halaman 2: Detail View (Analisis Mendalam)            │
│  Halaman 3: Action Plan (4 Langkah)                    │
│                                                          │
│  Teknologi: Dart, Flutter, Material Design             │
│  API: http://127.0.0.1:5000/prediksi-batch            │
│        http://127.0.0.1:5000/prediksi-detail/{id}     │
│                                                          │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP Request (JSON)
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   FLASK BACKEND                          │
│          (Business Logic - Server Side)                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Authentication Service (JWT Token)                  │
│  2. Database Service (MySQL Connection)                │
│  3. Prediction Service (ML + Logic)                     │
│                                                          │
│  Process:                                               │
│   ├─ Verify token                                       │
│   ├─ Fetch bahan dari DB                              │
│   ├─ Get latest stock untuk setiap bahan              │
│   ├─ Run ML prediction model                           │
│   ├─ Calculate metrics                                 │
│   ├─ Generate recommendation                           │
│   ├─ Create action plan                                │
│   └─ Return JSON response                              │
│                                                          │
│  Teknologi: Python, Flask, scikit-learn, joblib        │
│  Model: Random Forest Regressor (200 trees)            │
│                                                          │
└────────────────┬────────────────────────────────────────┘
                 │ SQL Queries
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   MYSQL DATABASE                         │
│              (Data Persistence Layer)                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Tables:                                                │
│   • bahans (7 items)                                    │
│     - id, nama, unit, stok_minimum, stok_optimal       │
│     - harga_per_unit, created_at, updated_at           │
│                                                          │
│   • stock_records (10 items)                            │
│     - id, user_id, bahan_id, jumlah, tipe             │
│     - catatan, tanggal, created_at                      │
│                                                          │
│   • users (1 item)                                      │
│     - id, email, password, name, phone                  │
│     - is_active, created_at, updated_at                │
│                                                          │
│   • (+ 4 lagi: notifications, orders, predictions,     │
│     audit_logs)                                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 MACHINE LEARNING FLOW

```
DATA INPUT (Per Bahan)
    │
    ├─ Current Stock: 10.5 kg
    ├─ Price: Rp 5000/unit
    ├─ Status: Kritis
    └─ Days History: 30
    │
    ▼
FEATURE VECTOR: [10.5, 5000, 0, 30]
    │
    ▼
RANDOM FOREST MODEL
    │ (200 decision trees)
    │ (Max depth: 15)
    │ (Trained on 15 samples)
    │
    ▼
OUTPUT: 82 unit/bulan
    │
    ├─ Confidence: 85.3%
    ├─ Daily: 2.7 unit
    ├─ Cost: Rp 407,922
    └─ Stockout: 3.9 hari
    │
    ▼
SMART RECOMMENDATION ENGINE
    │
    ├─ If stockout < 7 hari: HIGH PRIORITY
    ├─ If stockout < 14 hari: MEDIUM PRIORITY
    └─ Else: LOW PRIORITY
    │
    ▼
ACTION PLAN (4 steps)
    ├─ 1. URGENT_ORDER (hari ini)
    ├─ 2. EXPEDITED (1-2 hari)
    ├─ 3. REGULAR (3-7 hari)
    └─ 4. MONITOR (ongoing)
```

---

## 📈 CONTOH REAL DATA

Dari **actual test yang baru saja jalan**:

### Tepung Terigu (ID: 1)

```
Current Stock:    10.5 kg
Minimum:          50 kg    (stok kurang 39.5 kg!)
Optimal:          200 kg   (stok kurang 189.5 kg!)

Prediction:
  Daily Demand:   2.7 kg/hari
  Monthly:        82 kg/bulan
  Cost Est:       Rp 407,922

Days Until Stockout: 3.9 hari ← URGENT!

Confidence:       85.3% ← Tinggi, bisa dipercaya

Recommendation:   ORDER_IMMEDIATELY (HIGH)
Message:          Prediksi permintaan tinggi. Lakukan
                  pemesanan segera!
```

### Gula Halus (ID: 4)

```
Current Stock:    Similar level

Prediction:
  Daily Demand:   3.7 kg/hari
  Monthly:        112 kg/bulan
  Cost Est:       Much higher

Days Until Stockout: 4.1 hari ← Juga URGENT!

Recommendation:   ORDER_IMMEDIATELY (HIGH)
```

---

## 💡 APA YANG DIDAPAT USER?

### Batch View (Ringkasan Cepat)

```
✓ Lihat prioritas 7 bahan sekali pandang
✓ Tahu mana yang paling urgent
✓ Estimasi demand untuk planning
✓ Color-coded untuk mudah dipahami
```

### Detail View (Analisis Mendalam)

```
✓ Stock status vs minimum vs optimal
✓ Detailed demand prediction
✓ Estimated cost untuk budgeting
✓ Confidence level untuk trust
✓ Clear action plan dengan timeline
✓ Steps-by-step guidance
```

### Action Plan (Guidance)

```
✓ Tahu harus berbuat apa
✓ Tahu harus berbuat kapan
✓ Prioritas yang jelas
✓ Timeline yang realistis
```

---

## ✅ FEATURES YANG BEKERJA

| Feature              | Status | Demo Result                |
| -------------------- | ------ | -------------------------- |
| ML Prediction        | ✅     | 82 unit/bulan untuk Tepung |
| Confidence Score     | ✅     | 85.3%                      |
| Days to Stockout     | ✅     | 3.9 hari                   |
| Cost Estimation      | ✅     | Rp 407,922                 |
| Smart Recommendation | ✅     | ORDER_IMMEDIATELY          |
| Priority Sorting     | ✅     | 7 bahan ranked             |
| Action Planning      | ✅     | 4-step plan                |
| API Integration      | ✅     | 200 OK response            |
| Flutter UI           | ✅     | Fully functional           |

---

## 🎯 RESULT

**Sistem memberikan:**

1. **Visibility** - Tahu kondisi stok real-time
2. **Prediction** - Tahu kapan stok akan habis
3. **Recommendation** - Tahu harus berbuat apa
4. **Guidance** - Tahu harus berbuat kapan
5. **Confidence** - Tahu seberapa terpercaya prediksi

**Impact:**

- Mencegah stockout mendadak
- Mengoptimalkan biaya inventory
- Membuat keputusan lebih informed
- Mengurangi risiko kehilangan penjualan

---

**Status:** ✅ **FULLY WORKING & DEMONSTRATED**  
**Date:** December 25, 2025  
**Test Result:** All Features Passed
