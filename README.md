# Web Asupan - Platform Video Streaming

Sebuah platform video streaming dengan tampilan dark mode yang elegan, dibuat menggunakan Flask dan Bootstrap.

## Fitur Utama

### 1. Manajemen Video
- [x] Upload video (URL atau file)
- [x] Thumbnail otomatis dari video
- [x] Pengelompokan video berdasarkan kategori
- [x] Multiple tag untuk setiap video
- [x] Pencarian video berdasarkan judul
- [x] Tampilan video terbaru
- [x] Penghitungan views untuk setiap video
- [x] Pagination di semua halaman video

### 2. Menu Navigasi
- **Beranda**: Menampilkan semua video
- **Terbaru**: 12 video terbaru berdasarkan tanggal upload
- **Kategori**: Daftar kategori dengan jumlah video
- **Populer**: 12 video dengan views terbanyak
- **Pencarian**: Cari video berdasarkan judul

### 3. Panel Admin
- Login sistem untuk admin
- Manajemen video dan kategori
- Form upload video dengan pilihan kategori
- Daftar video dengan informasi lengkap
- CRUD operasi untuk video dan kategori

### 4. UI/UX
- Dark mode dengan aksen warna hijau
- Responsif di semua device
- Animasi hover yang smooth
- Loading yang optimal
- Navigasi yang intuitif

## Teknologi

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: Autentikasi admin

### Frontend
- **Bootstrap 5**: Framework CSS
- **Font Awesome**: Icon
- **Custom CSS**: Dark mode styling

### Database
- **SQLite**: Database lokal
- **Tabel**: Users, Videos, Categories

## Struktur Database

### Users
- id (Primary Key)
- username
- password_hash

### Categories
- id (Primary Key)
- name
- videos (Relationship)

### Videos
- id (Primary Key)
- title
- thumbnail_url
- video_url
- category_id (Foreign Key)
- views
- created_at

## Kredensial Admin
- Username: YADIRC
- Password: YadiRc120502

## Panduan Penggunaan

### 1. Instalasi
```bash
# Clone repository
git clone [repository-url]

# Masuk ke direktori
cd webasupan

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app.py
```

### 2. Mengakses Panel Admin
1. Buka http://localhost:5000/admin-login
2. Login dengan kredensial admin
3. Akses panel admin untuk mengelola konten

### 3. Menambah Video
1. Login sebagai admin
2. Klik "Tambah Video"
3. Isi form dengan:
   - Judul video
   - URL thumbnail
   - URL video
   - Pilih kategori
4. Klik "Tambah" untuk menyimpan

### 4. Mengelola Kategori
1. Login sebagai admin
2. Scroll ke bagian "Tambah Kategori"
3. Masukkan nama kategori
4. Klik "Tambah" untuk menyimpan

## Fitur Lengkap
### Manajemen Video
- [x] Upload video (URL atau file)
- [x] Thumbnail otomatis dari video
- [x] Pengelompokan video berdasarkan kategori
- [x] Multiple tag untuk setiap video
- [x] Pencarian video berdasarkan judul
- [x] Tampilan video terbaru
- [x] Penghitungan views untuk setiap video
- [x] Pagination di semua halaman video

### Kategori
- [x] Manajemen kategori (tambah, hapus)
- [x] Halaman khusus untuk setiap kategori
- [x] Dropdown menu kategori di navbar
- [x] Tampilan jumlah video per kategori

### Tag
- [x] Manajemen tag (tambah, hapus)
- [x] Multiple tag selection saat upload video
- [x] Halaman khusus untuk setiap tag
- [x] Tampilan jumlah video per tag
- [x] Delete tag menggunakan AJAX

### UI/UX
- [x] Responsive design menggunakan Bootstrap 5
- [x] Dark theme
- [x] Font Awesome icons
- [x] Card layout untuk video
- [x] Thumbnail dengan efek hover
- [x] Navbar yang rapi dengan highlight menu aktif
- [x] Flash messages untuk feedback
- [x] Loading state saat upload
- [x] Empty state saat tidak ada video
- [x] Konfirmasi sebelum hapus

### Admin
- [x] Login admin
- [x] Dashboard admin
- [x] Manajemen video
- [x] Manajemen kategori
- [x] Manajemen tag
- [x] Logout

### Manajemen Data
- [x] Hapus semua video sekaligus
- [x] Hapus semua kategori (termasuk video terkait)
- [x] Hapus semua tag
- [x] Konfirmasi sebelum penghapusan massal
- [x] Rollback jika terjadi error
- [x] Update UI secara otomatis setelah penghapusan
- [x] Feedback menggunakan alert

### Monetisasi
- [x] Integrasi Adsterra Popunder
- [x] Optimasi delay iklan (5 menit)
- [x] Batasan 3 popunder per session
- [x] Reset counter setiap 24 jam
- [x] Anti-AdBlock system
  - Deteksi cepat (1-2 detik)
  - Multiple detection methods
  - Overlay warning message
  - Prevent bypass attempts

### Development Mode
- [x] Toggle Development/Production mode
- [x] Disable iklan saat development
- [x] Status indikator di admin panel
- [x] Automatic mode detection
- [x] Safe testing environment

### Security
- [x] Admin area tanpa iklan
- [x] Protection dari ad fraud
- [x] Session management
- [x] Prevent overlay removal
- [x] Secure mode switching

## Catatan Pengembangan

### Perubahan Terakhir
1. Implementasi dark mode menyeluruh
2. Perbaikan struktur HTML dengan wrapper
3. Optimasi warna dan kontras
4. Penyesuaian responsivitas

### Todo List
1. Implementasi fitur komentar
2. Sistem rating video
3. Halaman profil user
4. Statistik view yang lebih detail
5. Sistem bookmark video

### Masalah yang Sudah Diperbaiki
1. Struktur database untuk kategori
2. Warna background yang tidak konsisten
3. Responsivitas di mobile device
4. Optimasi loading gambar

## Kontribusi
Silakan berkontribusi dengan membuat pull request atau melaporkan issues.

## Lisensi
Copyright 2025 Web Asupan. All rights reserved.
