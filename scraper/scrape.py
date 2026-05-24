import requests
import json
import os
from datetime import datetime, timedelta

URL = "https://magma.esdm.go.id/v1/gunung-api/laporan/search/q"

history_path = "../data/history.json"

now = datetime.now()
start = now - timedelta(days=7)

params = {
    "code": "IYA",
    "start": start.strftime("%Y-%m-%d"),
    "end": now.strftime("%Y-%m-%d")
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(URL, params=params, headers=headers)

data = res.json().get("data", [])

new_data = []

for item in data:

    raw = str(item).lower()

    new_data.append({
        "date": item.get("tanggal", now.strftime("%Y-%m-%d")),
        "time": item.get("jam", "00:00"),
        "status": item.get("status", "UNKNOWN"),

        "gempa": {
            "vulkanik_dalam": raw.count("vulkanik dalam"),
            "vulkanik_dangkal": raw.count("vulkanik dangkal"),
            "low_frequency": raw.count("low freq"),
            "tremor_harmonik": raw.count("tremor harmonik"),
            "tremor_menerus": raw.count("tremor terus"),
            "tornillo": raw.count("tornillo"),
            "hembusan": raw.count("hembusan"),
            "tektonik_lokal": raw.count("tektonik lokal"),
            "tektonik_jauh": raw.count("tektonik jauh"),
        }
    })

# load lama
old = []
if os.path.exists(history_path):
    old = json.load(open(history_path))

# merge
merged = new_data + old

# unique by date+time
unique = {}
for d in merged:
    key = d["date"] + d["time"]
    unique[key] = d

final = list(unique.values())

# sort newest first
final.sort(key=lambda x: (x["date"], x["time"]), reverse=True)

json.dump(final, open(history_path, "w"), indent=2)

print("SCRAPE DONE")
