# LK21 Android TV — Netflix Style (Leanback + FastAPI)

Proyek ini merupakan aplikasi streaming khusus **Android TV** dengan antarmuka dan navigasi bergaya **Netflix** (*10-foot UI*). Menggunakan arsitektur pemisahan antara **Backend Scraper (Python FastAPI)** dan **Frontend Native TV (Kotlin AndroidX Leanback + ExoPlayer)**.

---

## 🏗️ Struktur Arsitektur

```text
netflix_lk21_tv/
├── backend/                  # Server FastAPI (Penyedia Data & Scraper)
│   ├── main.py              # Endpoint API REST (/api/feed, /api/movie/{id})
│   ├── scraper.py           # Ekstraktor data LK21 + Engine Fallback
│   ├── requirements.txt     # Dependensi Python (FastAPI, Uvicorn, BeautifulSoup4)
│   └── run.bat              # Script jalan 1-klik untuk Windows
│
└── android_tv/               # Proyek Android Studio (Native Kotlin)
    ├── app/src/main/
    │   ├── AndroidManifest.xml # Konfigurasi Android TV & Banner 16:9
    │   ├── java/com/netflix/lk21tv/
    │   │   ├── models/        # MovieCard, CategoryFeed, MovieDetail
    │   │   ├── network/       # Retrofit Client (ApiClient.kt)
    │   │   └── ui/
    │   │       ├── MainActivity.kt      # Container Activity
    │   │       ├── MainFragment.kt      # Netflix Browse UI (Leanback)
    │   │       ├── CardPresenter.kt     # Kartu Poster + Efek Fokus Remote
    │   │       └── PlaybackActivity.kt  # Fullscreen ExoPlayer + Kontrol Remote D-Pad
    │   └── res/
    │       ├── drawable/      # Banner TV 16:9 & Logo Netflix Red
    │       ├── layout/        # Layout UI & Custom Player Control
    │       └── values/        # colors.xml (Netflix Red/Black), themes.xml
```

---

## 🚀 Langkah 1: Menjalankan Backend (Python FastAPI)

1. Buka folder `backend/`.
2. Klik ganda file `run.bat` (atau jalankan perintah berikut di terminal):
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. Cek browser Anda di `http://localhost:8000/docs` untuk melihat dokumentasi API interaktif.
4. **Cek Alamat IP Komputer Anda:**
   - Buka CMD/Terminal, ketik `ipconfig`.
   - Cari baris **IPv4 Address** pada adapter Wi-Fi Anda (misalnya: `192.168.1.15`).

---

## 📺 Langkah 2: Membuka & Menjalankan Android TV App

1. Buka **Android Studio**.
2. Pilih **Open** dan arahkan ke folder:
   `netflix_lk21_tv/android_tv/`
3. Tunggu proses *Gradle Sync* selesai.
4. Buka file:
   `app/src/main/java/com/netflix/lk21tv/network/ApiClient.kt`
   - Ganti `BASE_URL`:
     - Jika pakai **Android TV Emulator**: gunakan `"http://10.0.2.2:8000/"`
     - Jika pakai **Android TV Fisik (Smart TV / STB)**: ubah ke IP komputer Anda, contoh: `"http://192.168.1.15:8000/"` *(Pastikan TV dan Laptop terhubung ke Wi-Fi yang sama)*.
5. Klik **Run** (pilih perangkat Android TV Emulator atau Sambungkan TV via ADB).
6. Atau klik menu **Build > Build Bundle(s) / APK(s) > Build APK(s)** untuk menghasilkan file `.apk`.

---

## 🎮 Panduan Kontrol Remote Android TV

Aplikasi ini sudah dioptimalkan 100% untuk remote kontrol TV (D-Pad):

| Tombol Remote | Fungsi |
|---|---|
| **Panah Atas / Bawah** | Berpindah antar baris kategori (Trending, Populer, Action, Horor, dll.) |
| **Panah Kiri / Kanan** | Menggeser daftar poster film ke samping |
| **Fokus Poster (Hover)** | Latar belakang layar TV otomatis berganti poster film yang disorot (mirip Netflix) |
| **Tombol OK / Enter** | Membuka dan memutar film pilihan secara fullscreen |
| **Panah Kiri (Saat Putar)** | Memundurkan video 10 detik (*Rewind*) |
| **Panah Kanan (Saat Putar)** | Memajukan video 10 detik (*Fast Forward*) |
| **Tombol OK (Saat Putar)** | Jeda (*Pause*) / Lanjutkan (*Play*) |
| **Tombol Back** | Keluar dari pemutar video kembali ke daftar film |
