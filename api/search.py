from http.server import BaseHTTPRequestHandler
from pathlib import Path
import json

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

DATA_FILE = DATA_DIR / "file_data.csv"


def json_response(handler, status_code, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError("File data tidak ditemukan di folder data.")

    return pd.read_csv(DATA_FILE).fillna("")


def search_data(query):
    df = load_data()

    # Ganti nama kolom ini sesuai file data masing-masing.
    title_column = "judul"
    content_column = "isi"

    if title_column not in df.columns or content_column not in df.columns:
        raise ValueError("Nama kolom belum sesuai dengan file data.")

    query_lower = query.lower()
    results = []

    for index, row in df.iterrows():
        title = str(row[title_column])
        content = str(row[content_column])
        combined_text = f"{title} {content}".lower()

        if query_lower in combined_text:
            results.append(
                {
                    "id": int(index + 1),
                    "title": title,
                    "snippet": content[:250],
                }
            )

    return results[:10]


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        json_response(self, 200, {"ok": True})

    def do_GET(self):
        json_response(
            self,
            200,
            {
                "message": "Gunakan POST /api/search",
                "example": {"query": "contoh"},
            },
        )

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(raw_body or "{}")

            query = str(payload.get("query", "")).strip()
            if not query:
                json_response(self, 400, {"detail": "Query tidak boleh kosong."})
                return

            results = search_data(query)

            json_response(
                self,
                200,
                {
                    "query": query,
                    "total_results": len(results),
                    "results": results,
                },
            )
        except Exception as error:
            json_response(self, 500, {"detail": str(error)})

