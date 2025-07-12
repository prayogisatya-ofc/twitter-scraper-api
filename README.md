# Twitter Scraper API

Selamat datang di **Twitter Scraper API**! Proyek ini menyediakan API yang kuat dan fleksibel untuk melakukan scraping data tweet berdasarkan kueri pencarian. Dibangun dengan Flask, sistem ini dirancang untuk efisiensi, keamanan, dan kemudahan penggunaan, baik untuk pengembangan lokal maupun deployment di shared hosting.

## Fitur Utama

### 1. Scraping Twitter yang Efisien
- Menggunakan library `twikit` untuk interaksi yang handal dengan Twitter.
- Mendukung pencarian tweet berdasarkan kueri tertentu.
- Dilengkapi dengan mekanisme anti-deteksi (`random_delay`) untuk mengurangi risiko pemblokiran oleh Twitter.
- Mengembalikan data tweet yang relevan (username, konten, gambar profil, waktu pembuatan).

### 2. Manajemen Sesi Login Fleksibel
Sebuah skrip Python terpisah, `login_session_manager.py`, disediakan untuk mengelola sesi login Twitter. Ini memungkinkan Anda untuk:
- Melakukan login dan menyimpan sesi ke `twitter_session.json` melalui terminal.
- Memuat sesi yang sudah ada dari `twitter_session.json`.
- Mengambil kredensial login dari file `.env` secara otomatis atau meminta input manual jika tidak ditemukan.

**Cara Penggunaan `login_session_manager.py`:**
```bash
python3 login_session_manager.py
```

### 3. Autentikasi API Key untuk Keamanan
Untuk mengamankan akses API dari aplikasi eksternal, sistem ini mengimplementasikan autentikasi API Key:
- Endpoint `/scrape` dilindungi oleh decorator `@require_api_key`.
- Setiap permintaan ke endpoint ini harus menyertakan header `X-API-Key` dengan nilai yang valid.

**Contoh Penggunaan API dengan API Key:**
```bash
curl -X POST http://localhost:5001/api/twitter/scrape \
  -H "Content-Type: application/json" \
  -H "X-API-Key: twitter_scraper_api_key_2024" \
  -d '{"query": "python programming"}'
```

### 4. Konfigurasi Lingkungan yang Aman
- **Kredensial di `.env`**: Semua kredensial sensitif (username, email, password Twitter, API Key) disimpan dalam file `.env` untuk keamanan yang lebih baik dan kemudahan konfigurasi.
  Contoh `.env`:
  ```
  TWITTER_USERNAME=your_twitter_username
  TWITTER_EMAIL=your_twitter_email
  TWITTER_PASSWORD=your_twitter_password
  API_KEY=your_secret_api_key
  ```

### 5. Dukungan Deployment Fleksibel
- **File WSGI**: File `passenger_wsgi.py` dan `wsgi.py` disertakan untuk mendukung deployment di shared hosting yang menggunakan Passenger atau server WSGI standar lainnya.
- **Pembersihan Kode**: File dan direktori yang tidak terpakai (`src/database/app.db`, `src/static/favicon.ico`, `src/static/index.html`, semua `__pycache__`) telah dihapus untuk menjaga kebersihan proyek.

## Struktur Proyek

```
twitter-scraper-api/
├── .env                        # Kredensial dan konfigurasi lingkungan
├── .gitignore                  # File yang diabaikan oleh Git
├── login_session_manager.py    # Skrip untuk manajemen sesi login Twitter
├── passenger_wsgi.py           # Entry point WSGI untuk Passenger
├── wsgi.py                     # Entry point WSGI standar
├── requirements.txt            # Daftar dependensi Python
├── README.md                   # Dokumentasi proyek ini
├── src/
│   ├── main.py                 # Aplikasi Flask utama
│   ├── routes/
│   │   ├── twitter_scraper.py  # Endpoint scraping Twitter (memerlukan API Key)
│   ├── static/
│   │   └── index.html          # Halaman awal aplikasi (tidak digunakan)
│   ├── utils/
│   │   ├── anti_detection.py   # Utilitas untuk anti-deteksi scraping
│   │   └── auth.py             # Utilitas untuk autentikasi API Key
└── twitter_session.json       # File sesi Twitter (dibuat otomatis setelah login)
```

## Instalasi dan Penggunaan

1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/prayogisatya-ofc/twitter-scraper-api.git
    cd twitter-scraper-api
    ```
2.  **Buat dan aktifkan virtual environment (opsional tapi direkomendasikan):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instal dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Buat file `.env`** di root proyek dan isi dengan kredensial Anda (lihat bagian Konfigurasi Lingkungan yang Aman di atas).
5.  **Buat sesi login Twitter** menggunakan `login_session_manager.py`:
    ```bash
    python3 login_session_manager.py
    ```
    Ikuti petunjuk di terminal.
6.  **Jalankan aplikasi Flask:**
    ```bash
    python3 src/main.py
    ```
    Aplikasi akan berjalan di `http://127.0.0.1:5001` (atau port lain yang dikonfigurasi).
7.  **Uji API** menggunakan `curl` atau Postman (lihat contoh di bagian Autentikasi API Key).

## Kontribusi

Kami menyambut kontribusi! Jika Anda memiliki ide, perbaikan bug, atau fitur baru, silakan buka _issue_ atau kirim _pull request_.