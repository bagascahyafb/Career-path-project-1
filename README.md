# Career Path Recommender for Data Professionals 🚀

## 📋 Table of Contents
- [Latar Belakang](#-latar-belakang)
- [Fitur Utama](#-fitur-utama)
- [Demo Aplikasi](#-demo-aplikasi)
- [Instalasi & Penggunaan](#-instalasi--penggunaan)
- [Metodologi](#-metodologi)
- [Struktur Proyek](#-struktur-proyek)
- [Pengembang](#-pengembang)

---

## 💡 Latar Belakang

Industri data science berkembang dengan kecepatan yang luar biasa. Setiap tahun muncul *tools*, *library*, dan *framework* baru. Bagi mahasiswa yang baru lulus atau profesional yang ingin berpindah karir, pertanyaan terbesarnya sering kali bukan "bagaimana cara belajar", melainkan **"apa yang harus dipelajari selanjutnya agar relevan?"**

Proyek ini lahir untuk menjawab kebingungan tersebut. Alih-alih memberikan saran generik, sistem ini menggunakan data riil dari **25.000+ praktisi data** di seluruh dunia (Kaggle Survey 2021) untuk memberikan rekomendasi jalur pembelajaran yang dipersonalisasi sesuai dengan cita-cita karir pengguna.

## ✨ Fitur Utama

* **Rekomendasi Sadar Konteks (Context-Aware):** Saran yang diberikan disesuaikan dengan jabatan (*job title*) dan tingkat pengalaman pengguna. Rekomendasi untuk seorang *Data Analyst* junior akan berbeda dengan *Machine Learning Engineer* senior.
* **Sistem Rekomendasi Hybrid:** Menggabungkan kekuatan *Collaborative Filtering* untuk menemukan pola keahlian tersembunyi dan *Content-Based Filtering* untuk personalisasi awal.
* **Solusi "Cold-Start":** Bagi pengguna baru yang belum memiliki keahlian teknis, sistem menyediakan "Starter Pack" berisi *skill* fundamental yang paling banyak digunakan di jalur karir pilihan mereka.
* **Antarmuka Interaktif:** Aplikasi web berbasis Streamlit yang mudah digunakan untuk input profil dan melihat hasil rekomendasi secara instan.

## 🖥️ Demo Aplikasi

*(Tempatkan screenshot atau GIF aplikasi Anda di sini nanti)*
1.  **Halaman Input:** Pengguna memasukkan jabatan, pengalaman, dan *skill* yang sudah dikuasai.
2.  **Halaman Hasil:** Sistem menampilkan 10 rekomendasi teratas lengkap dengan kategori *skill*-nya (misal: Bahasa Pemrograman, Library ML, Platform Cloud).

## 🛠️ Instalasi & Penggunaan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda:

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/username-anda/career-path-recommender.git](https://github.com/username-anda/career-path-recommender.git)
    cd career-path-recommender
    ```

2.  **Buat virtual environment (opsional tapi disarankan):**
    ```bash
    python -m venv venv
    # Untuk Windows:
    venv\Scripts\activate
    # Untuk Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi Streamlit:**
    Pastikan Anda berada di root folder proyek, lalu jalankan:
    ```bash
    streamlit run app/1_Formulir_Input.py
    ```

## 🔬 Metodologi

Sistem ini dibangun melalui beberapa tahapan iteratif:

1.  **Data Preprocessing:** Pembersihan data survei Kaggle yang kompleks, termasuk *one-hot encoding* untuk fitur kategorikal dan pembuatan matriks interaksi *user-skill*.
2.  **Contextual Pre-Filtering (KCR-Lite):** Implementasi logika *pre-filtering* di mana sistem secara dinamis membentuk "squad" (kelompok pengguna referensi) yang relevan dengan konteks jabatan dan pengalaman pengguna saat ini.
3.  **Model Generation:**
    * Jika *squad* cukup besar (>20), sistem membentuk matriks kemiripan (*cosine similarity*) baru secara *on-the-fly* untuk rekomendasi yang sangat spesifik.
    * Jika *squad* terlalu kecil, sistem menggunakan model global sebagai *fallback* untuk menjaga stabilitas rekomendasi.
4.  **Evaluasi:** Model dievaluasi menggunakan metrik **Precision@K** dan **Recall@K** secara offline untuk memastikan relevansi rekomendasi yang dihasilkan.

## 📂 Struktur Proyek
career-path-recommender/ 
├── app/ 
│├── 1_Formulir_Input.py # Halaman utama aplikasi 
│ └── pages/ 
│ └── 2_Hasil_Rekomendasi.py # Halaman logika & hasil rekomendasi 
├── data/ 
│├── kaggle_survey_2021_responses.csv # Data mentah (tidak di-upload ke git) 
│ └── ... (file CSV hasil olahan) 
├── notebooks/ 
│ ├── 1-data-preprocessing.ipynb 
│ ├── 2-content-based-engine.ipynb 
│ ├── 3-collaborative-engine.ipynb 
│ └── 5-evaluation.ipynb ├── saved_models/ 
│ └── ... (file model .joblib) 
├── requirements.txt # Daftar library Python 
└── README.md # Dokumentasi proyek
## 👨‍💻 Pengembang

**Bagas Cahya Fajar Bastian**
*Mahasiswa Sains Data | Aspiring Data Scientist*

Dibuat menggunakan Python dan Streamlit.