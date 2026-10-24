# PROPOSAL PROJECT & SPESIFIKASI KEBUTUHAN PERANGKAT LUNAK (SRS)

## TradeHub: Platform E-Commerce C2C Marketplace Jual Beli Barang Online

| | |
|---|---|
| **Mata Kuliah / Tugas** | Web Framework — Tugas Ke-2 |
| **Nama Project** | TradeHub Marketplace |
| **Tech Stack Utama** | Frontend: Next.js \| Backend: FastAPI \| Database: PostgreSQL/MySQL |
| **Status & Tanggal** | Final Draft — Siap Dikumpulkan (September 2026) |

---

## 1. Pendahuluan & Proposal Project

### 1.1 Judul Project

TradeHub: Platform E-Commerce C2C Marketplace Jual Beli Barang Online

### 1.2 Justifikasi Masalah & Latar Belakang

Perkembangan perdagangan digital di Indonesia mendorong tingginya aktivitas jual beli antar individu (Consumer-to-Consumer / C2C) serta Usaha Mikro, Kecil, dan Menengah (UMKM). Namun, banyak penjual independen yang masih mengandalkan platform media sosial atau aplikasi pesan instan untuk melayani pembeli. Metode konvensional ini memiliki beberapa kelemahan mendasar:

- **Risiko Keamanan & Transaksi:** Transaksinya rentan terhadap penipuan karena tidak adanya sistem pencatatan transaksi yang terverifikasi dan transparan.
- **Pengelolaan Stok Manual:** Penjual sering kesulitan mengelola jumlah stok barang secara aktual, menyebabkan risiko double-selling atau pesanan dibatalkan.
- **Pengalaman Pengguna Cenderung Buruk:** Pembeli kesulitan melakukan pencarian barang spesifik, penyaringan harga, serta memantau status pengiriman secara real-time.

### 1.3 Solusi yang Ditawarkan

TradeHub hadir sebagai solusi terpusat berupa platform marketplace berbasis web yang menyediakan ekosistem terintegrasi untuk Pembeli, Penjual, dan Admin. Sistem ini mencakup Katalog Produk Dinamis, Manajemen Toko & Stok bagi Penjual, Keranjang Belanja (Shopping Cart), Checkout Transaksi Terstruktur, serta Dashboard Analytics.

### 1.4 Justifikasi Pemilihan Tech Stack

> **Mengapa Kombinasi Tech Stack Ini Efektif?**
> Kombinasi Next.js, FastAPI, dan PostgreSQL/MySQL dipilih untuk menjamin performa tinggi, efisiensi pengembangan, keamanan data finansial, serta kemudahan skalabilitas sistem di masa depan.

| Layer | Teknologi | Justifikasi Teknis & Alasan Pemilihan |
|---|---|---|
| **Frontend** | **Next.js (React)** | 1. Server-Side Rendering (SSR) & SSG untuk optimasi SEO produk agar mudah terindeks Google.<br>2. Performance tinggi dengan App Router, caching bawaan, dan loading visual yang cepat.<br>3. Modularitas komponen React mempermudah pembuatan UI e-commerce yang kompleks. |
| **Backend** | **FastAPI (Python)** | 1. Performa sangat tinggi berbasis ASGI (Asynchronous Server Gateway Interface).<br>2. Validasi data otomatis menggunakan Pydantic untuk menjamin integritas payload request.<br>3. Generasi dokumentasi API interaktif otomatis (Swagger UI/OpenAPI) mempercepat kolaborasi tim. |
| **Database** | **PostgreSQL / MySQL** | 1. Database Relasional (RDBMS) bersertifikasi ACID Compliance untuk menjamin transaksi finansial dan stok barang konsisten.<br>2. Kemampuan handling transaksi berskala besar, indexing cepat, dan fitur Row-Level Locking untuk mencegah stok minus. |

---

## 2. Deskripsi Umum Sistem (System Overview)

### 2.1 Ruang Lingkup Sistem (Scope)

Platform TradeHub mencakup seluruh alur bisnis e-commerce C2C modern. Batasan sistem meliputi:

- **Manajemen Akun:** Modul pendaftaran pengguna, otentikasi aman via JSON Web Token (JWT), dan pengelolaan profil pengguna.
- **Manajemen Toko & Katalog:** Modul bagi penjual untuk membuka toko, menambah produk, mengunggah foto, mengatur kategori, serta memperbarui kuantitas stok secara real-time.
- **Pencarian & Penjelajahan:** Pencarian produk berbasis kata kunci, filter kategori, rentang harga, serta pengurutan (sorting) produk.
- **Transaksi & Pesanan:** Pengelolaan keranjang belanja interaktif dan pemrosesan checkout pesanan (Order Management).
- **Dashboard Administrasi:** Panel pengawasan bagi admin untuk memantau aktivitas transaksi, verifikasi toko, dan penanganan produk yang melanggar aturan.

### 2.2 Profil Pengguna (User Personas)

Sistem ini mengidentifikasi tiga aktor utama yang berinteraksi dengan platform TradeHub:

| Aktor | Peran Utama | Hak Akses Utama dalam Sistem |
|---|---|---|
| **Pembeli (Buyer)** | Mencari dan membeli barang kebutuhan secara online. | Registrasi/Login, Browsing & Search, Tambah ke Cart, Checkout Pesanan, Lacak Status Order, Beri Ulasan. |
| **Penjual (Seller)** | Mengelola toko pribadi dan memasarkan produk. | Buka Toko, Upload/Edit/Hapus Produk, Kelola Stok, Update Status Pengiriman, Lihat Laporan Penjualan. |
| **Admin Platform** | Memelihara ketertiban dan keberlangsungan sistem. | Kelola User & Toko, Verifikasi/Moderate Produk, Suspend Akun Melanggar, Lihat Ringkasan Statistik Platform. |

---

## 3. Kebutuhan Fungsional (Functional Requirements)

Kebutuhan fungsional mendefinisikan layanan dan fitur spesifik yang harus disediakan oleh sistem TradeHub:

| Kode FR | Modul / Fitur | Aktor | Deskripsi Spesifikasi Kebutuhan |
|---|---|---|---|
| **FR-01** | Autentikasi & Akun | User, Seller | Sistem harus menyediakan fasilitas pendaftaran akun, login, logout, dan pembaruan profil menggunakan enkripsi kata sandi dan JWT token. |
| **FR-02** | Manajemen Produk | Penjual | Sistem harus memungkinkan Penjual menambah, mengubah, dan menghapus barang (nama, deskripsi, harga, stok, foto, dan kategori). |
| **FR-03** | Pencarian & Filtering | Pembeli | Sistem harus menyediakan pencarian produk real-time berdasarkan kata kunci, penyaringan kategori, rentang harga, serta pengurutan produk. |
| **FR-04** | Keranjang Belanja | Pembeli | Sistem harus memungkinkan Pembeli menambah barang ke keranjang, mengubah kuantitas, memilih item yang dibeli, atau menghapus item. |
| **FR-05** | Checkout Transaksi | Pembeli | Sistem harus memproses checkout pesanan, menghitung total biaya, menyimpan alamat pengiriman, dan menghasilkan invoice order unik. |
| **FR-06** | Manajemen Pesanan | Penjual, Pembeli | Sistem harus memungkinkan Penjual memperbarui status pesanan (Diproses, Dikirim, Selesai) dan Pembeli melacak status pengiriman. |
| **FR-07** | Dashboard Administrasi | Admin | Sistem harus menyediakan dashboard untuk Admin memantau jumlah total user, transaksi, serta memblokir produk/toko yang bermasalah. |

---

## 4. Kebutuhan Non-Fungsional (Non-Functional Requirements)

Kebutuhan non-fungsional memastikan kualitas, performa, dan tingkat keamanan aplikasi TradeHub terjamin:

| Kode NFR | Kategori Kualitas | Deskripsi Spesifikasi Non-Fungsional |
|---|---|---|
| **NFR-01** | Performance & Latency | Respon API dari backend FastAPI untuk query pencarian produk dan detail katalog tidak boleh melebihi 300 ms pada beban normal. |
| **NFR-02** | Usability & SEO | Tampilan antarmuka Next.js wajib fully responsive (nyaman diakses via Smartphone maupun PC) serta memenuhi standar SEO Google (Core Web Vitals). |
| **NFR-03** | Security & Privacy | Seluruh password wajib dienkripsi menggunakan algoritma Bcrypt. Komunikasi API menggunakan protokol HTTPS dan otentikasi berbasis JSON Web Token (JWT). |
| **NFR-04** | Reliability & ACID | Database PostgreSQL/MySQL harus mempertahankan konsistensi data transaksi (ACID compliance) dan menerapkan database locking saat stok produk di-checkout bersamaan. |

---

## 5. Arsitektur Sistem & Spesifikasi Teknis

### 5.1 Diagram Arsitektur Multi-Tier

Sistem TradeHub menerapkan arsitektur *Decoupled Frontend-Backend* untuk memisahkan logika tampilan dan logika bisnis secara jelas:

```text
[ CLIENT / BROWSER DEVICE ]
       │
       │  HTTP / HTTPS Requests
       ▼
[ FRONTEND TIER: Next.js (React Framework) ]
  • UI Components (Tailwind CSS)
  • Server-Side Rendering (SSR) & Client State Management
       │
       │  REST API Calls (JSON payloads / Bearer JWT)
       ▼
[ BACKEND TIER: FastAPI (Python ASGI Framework) ]
  • Router & Controller Logic
  • Pydantic Schema Validation & Authentication Middleware
  • SQLAlchemy / SQLModel ORM Layer
       │
       │  SQL Queries / Prepared Statements
       ▼
[ DATABASE TIER: PostgreSQL / MySQL ]
  • Relational Tables (Users, Stores, Products, Orders, Carts)
```

### 5.2 Spesifikasi API Endpoints Utama (FastAPI)

Berikut adalah draf desain endpoint RESTful API utama yang disediakan oleh backend FastAPI:

| HTTP Method | Endpoint Path | Modul API | Fungsi / Deskripsi |
|---|---|---|---|
| **POST** | `/api/v1/auth/register` | Auth | Registrasi user baru (Buyer/Seller). |
| **POST** | `/api/v1/auth/login` | Auth | Autentikasi & pengembalian JWT access token. |
| **GET** | `/api/v1/products` | Produk | Mendapatkan daftar produk dengan query filter & search. |
| **POST** | `/api/v1/products` | Produk | Menambah produk baru (Memerlukan token Seller). |
| **POST** | `/api/v1/cart/items` | Keranjang | Menambahkan item produk ke keranjang belanja user. |
| **POST** | `/api/v1/orders/checkout` | Transaksi | Membuat pesanan baru dan mengurangi kuantitas stok. |

### 5.3 Skema Basis Data Relasional (Data Dictionary)

Struktur tabel utama dalam basis data PostgreSQL/MySQL dirancang sebagai berikut:

- **Tabel `users`:** Menyimpan data identitas pengguna, hashed password, email, dan role (buyer/seller/admin).
- **Tabel `stores`:** Menyimpan profil toko milik penjual (nama toko, deskripsi, alamat).
- **Tabel `products`:** Menyimpan data barang, harga, jumlah stok, kategori_id, dan store_id.
- **Tabel `orders` & `order_items`:** Menyimpan riwayat transaksi, total pembayaran, alamat tujuan, dan status pengiriman.

---

## 6. Rencana Kerja Kelompok & Jadwal Eksekusi

Untuk memastikan pengerjaan tepat waktu sebelum kuliah besok, pembagian tugas kelompok diatur sebagai berikut:

| Penanggung Jawab | Fokus Pengerjaan Tugas | Output Target |
|---|---|---|
| **Anggota 1** | Penyusunan Cover, Latar Belakang, Justifikasi Judul & Tech Stack | Dokumen Bagian Bab 1 & Bab 2 Rapi |
| **Anggota 2** | Detailing Kebutuhan Fungsional (FR) & Non-Fungsional (NFR) | Tabel Spesifikasi FR & NFR Lengkap |
| **Anggota 3** | Perancangan Arsitektur Sistem, API Endpoints, & Database Schema | Diagram & Tabel Teknis Bab 5 Completed |
