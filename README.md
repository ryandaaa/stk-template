# STK Vercel Python Template

Template minimal untuk website HTML statis dengan Python API di Vercel.

## Struktur

```text
.
├── api/
│   ├── health.py
│   └── search.py
├── data/
│   └── .gitkeep
├── index.html
├── requirements.txt
└── vercel.json
```

## Cara Pakai

1. Masukkan file data ke folder `data/`.
2. Ubah nama file dan nama kolom di `api/search.py`.
3. Deploy ke Vercel.

Bagian yang biasanya diubah:

```python
DATA_FILE = DATA_DIR / "file_data.csv"
title_column = "judul"
content_column = "isi"
```

## Endpoint

```text
GET  /api/health
POST /api/search
```

