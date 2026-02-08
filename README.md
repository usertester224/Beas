# Beas

Downloader sederhana berbasis `yt-dlp` dengan opsi kirim hasil ke Telegram melalui MTProto (hingga 2GB per file, tergantung batas Telegram).

## Persiapan

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Penggunaan

```bash
python downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Opsi tambahan:

```bash
# Simpan ke folder tertentu
python downloader.py "URL" --output-dir hasil

# Pilih format
python downloader.py "URL" --format "bestvideo+bestaudio"

# Ekstrak audio mp3
python downloader.py "URL" --audio

# Hindari playlist
python downloader.py "URL" --no-playlist
```

## Kirim ke Telegram (MTProto)

Siapkan kredensial Telegram (API ID & API Hash) dari https://my.telegram.org.
Buat sesi MTProto (StringSession) dengan Telethon, contoh singkat:

```bash
python - <<'PY'
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("API ID: "))
api_hash = input("API Hash: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
PY
```

Set environment variable berikut di VPS:

```bash
export TG_API_ID="123456"
export TG_API_HASH="your_api_hash"
export TG_SESSION="your_string_session"
```

Lalu jalankan:

```bash
python downloader.py "URL" --telegram
```

Opsional override chat tujuan (default Saved Messages):

```bash
python downloader.py "URL" --telegram --telegram-chat "@nama_channel"
```