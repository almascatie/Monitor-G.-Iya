import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

URL = "https://magma.esdm.go.id/v1/gunung-api/laporan/search/q"

end = datetime.now()
start = end - timedelta(days=7)

params = {
    "code": "IYA",
    "start": start.strftime("%Y-%m-%d"),
    "end": end.strftime("%Y-%m-%d")
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(URL, params=params, headers=headers, timeout=30)

print("STATUS:", res.status_code)

html = res.text

# simpan debug
with open("../data/debug.html", "w", encoding="utf-8") as f:
    f.write(html)

soup = BeautifulSoup(html, "html.parser")

history = []

# ambil semua text
text = soup.get_text("\n")

# parsing sederhana
lines = text.splitlines()

for line in lines:

    line = line.strip()

    if len(line) < 10:
        continue

    # cari kata penting
    if "Level" in line or "WASPADA" in line:

        history.append({
            "date": str(end.date()),
            "status": line,
            "gempa": line.lower().count("gempa"),
            "raw": line
        })

# fallback kalau kosong
if len(history) == 0:

    history.append({
        "date": str(end.date()),
        "status": "DATA TIDAK TERBACA",
        "gempa": 0,
        "raw": text[:500]
    })

latest = history[0]

with open("../data/history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

with open("../data/latest.json", "w", encoding="utf-8") as f:
    json.dump(latest, f, indent=2, ensure_ascii=False)

print("SCRAPING DONE")
