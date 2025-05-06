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
- **Tabel**: Users, Videos, Categories, Tags

### Monetisasi
- **Adsterra**: Platform iklan
  - Banner Ads
  - Social Bar
  - Popunder

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

### Tags
- id (Primary Key)
- name
- videos (Many-to-Many Relationship)

## Kredensial Admin
- Username: YADIRC
- Password: YadiRc120502

## Panduan Instalasi

### 1. Clone Repository
```bash
# Clone repository
git clone https://github.com/XBOLDASUPAN/webasupan.git

# Masuk ke direktori
cd webasupan
```

### 2. Setup Local Development
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Buat direktori yang diperlukan
mkdir -p static/uploads
mkdir -p instance

# Jalankan aplikasi
python app.py
```

### 3. Deploy ke PythonAnywhere

1. Buat akun di PythonAnywhere
2. Buka Bash console dan jalankan:
```bash
# Clone repository
git clone https://github.com/XBOLDASUPAN/webasupan.git
cd webasupan

# Setup virtual environment
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Buat direktori
mkdir -p static/uploads
mkdir -p instance

# Setup database
python3
```

3. Di Python shell:
```python
from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Buat semua tabel
    db.create_all()
    
    # Buat user admin
    admin = User.query.filter_by(username='YADIRC').first()
    if not admin:
        admin = User(username='YADIRC')
        admin.password_hash = generate_password_hash('YadiRc120502')
        db.session.add(admin)
        db.session.commit()
```

4. Set permissions:
```bash
chmod 755 static/uploads
chmod 755 instance
```

5. Konfigurasi Web App di PythonAnywhere:
   - Source code: `/home/username/webasupan`
   - Working directory: `/home/username/webasupan`
   - Virtual env: `/home/username/webasupan/venv`
   - WSGI file: Gunakan Flask default template

6. Reload web app

### 4. Konfigurasi Iklan

1. Daftar di [Adsterra](https://adsterra.com)
2. Dapatkan kode untuk:
   - Banner Ads
   - Social Bar
   - Popunder
3. Update kode di `templates/base.html`
4. Nonaktifkan development mode di panel admin

## Penggunaan

### 1. Mengakses Panel Admin
1. Buka `/admin-login`
2. Login dengan kredensial admin
3. Akses panel admin untuk mengelola konten

### 2. Menambah Video
1. Login sebagai admin
2. Klik "Tambah Video"
3. Isi form dengan:
   - Judul video
   - URL thumbnail
   - URL video
   - Pilih kategori
   - Pilih tag (opsional)
4. Klik "Tambah" untuk menyimpan

### 3. Mengelola Kategori
1. Login sebagai admin
2. Scroll ke bagian "Kelola Kategori"
3. Masukkan nama kategori
4. Klik "Tambah" untuk menyimpan

### 4. Mengelola Tag
1. Login sebagai admin
2. Scroll ke bagian "Kelola Tag"
3. Masukkan nama tag
4. Klik "Tambah" untuk menyimpan

## Troubleshooting

### Error yang Umum

1. **ModuleNotFoundError: No module named 'flask'**
   - Pastikan virtual environment aktif
   - Install ulang requirements

2. **No such table: video**
   - Jalankan `db.create_all()` di Python shell

3. **Permission Error**
   - Set permissions untuk folder uploads dan instance

4. **Iklan Tidak Muncul**
   - Pastikan development mode nonaktif
   - Periksa kode iklan di base.html
   - Nonaktifkan ad blocker

## Maintenance

### Backup Database
```bash
cd instance
cp videos.db videos.db.backup
```

### Update Aplikasi
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
```

## Lisensi
MIT License - Lihat file LICENSE untuk detail

## Kontak
- GitHub: [@XBOLDASUPAN](https://github.com/XBOLDASUPAN)
- PythonAnywhere: [webasupan.pythonanywhere.com](https://webasupan.pythonanywhere.com)
