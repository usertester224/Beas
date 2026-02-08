# Troubleshooting

## Kenapa `pip install -r requirements.txt` gagal?

Pada lingkungan ini, `pip` tidak bisa mengakses PyPI karena koneksi proxy memblokir akses (HTTP 403). Akibatnya, `pip` tidak dapat menemukan paket `yt-dlp` sehingga instalasi gagal. Detail error bisa dilihat di log berikut.

Lihat log lengkap: `docs/pip-install.log`.