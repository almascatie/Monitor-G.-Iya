import requests
import json
from datetime import datetime, timedelta

URL = "https://magma.esdm.go.id/v1/gunung-api/laporan/search/q"

end = datetime.now()
start = end - timedelta(days=7)

params = {
    "code": "IYA",
    "start": start.strftime("%Y-%m-%d"),
    "end": end.strftime("%Y-%m-%d")
}

res = requests.get(URL, params=params)

data = res.json()

history = []

for item in data.get("data", []):
    history.append({
        "date": item.get("tanggal") or item.get("date"),
        "status": item.get("status", "UNKNOWN"),
        "gempa": str(item).lower().count("gempa")
    })

latest = history[0] if history else {}

with open("../data/history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

with open("../data/latest.json", "w", encoding="utf-8") as f:
    json.dump(latest, f, indent=2, ensure_ascii=False)

print("Scraping selesai")
