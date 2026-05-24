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

response = requests.get(URL, params=params)

raw = response.json()

history = []

for item in raw.get("data", []):

    laporan = item.get("laporan", "")

    gempa = laporan.lower().count("gempa")

    status = item.get("status", "UNKNOWN")

    date = item.get("date", "")

    history.append({
        "date": date,
        "status": status,
        "gempa": gempa
    })

latest = history[0] if history else {}

with open("../data/history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

with open("../data/latest.json", "w", encoding="utf-8") as f:
    json.dump(latest, f, indent=2, ensure_ascii=False)

print("Data berhasil diperbarui")
