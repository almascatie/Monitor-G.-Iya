import requests
import json
import os
from datetime import datetime, timedelta

URL = "https://magma.esdm.go.id/v1/gunung-api/laporan/search/q"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/html"
}

now = datetime.now()
start = now - timedelta(days=7)

params = {
    "code": "IYA",
    "start": start.strftime("%Y-%m-%d"),
    "end": now.strftime("%Y-%m-%d")
}

res = requests.get(URL, params=params, headers=headers)

print("STATUS:", res.status_code)
print("CONTENT-TYPE:", res.headers.get("content-type"))

try:
    data = res.json()
except:
    print("JSON FAIL → fallback HTML")
    data = []

# debug simpan response mentah
os.makedirs("data", exist_ok=True)
with open("data/debug_response.txt", "w", encoding="utf-8") as f:
    f.write(res.text)

history = []

if isinstance(data, dict):
    items = data.get("data", [])
else:
    items = data

for item in items:

    history.append({
        "date": item.get("tanggal", ""),
        "time": item.get("jam", ""),
        "status": item.get("status", "UNKNOWN"),
        "gempa": {
            "vulkanik_dalam": 0,
            "vulkanik_dangkal": 0,
            "low_frequency": 0,
            "tremor_harmonik": 0,
            "tremor_menerus": 0,
            "tornillo": 0,
            "hembusan": 0,
            "tektonik_lokal": 0,
            "tektonik_jauh": 0,
        }
    })

os.makedirs("data", exist_ok=True)

with open("data/history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2)

print("DONE:", len(history))
