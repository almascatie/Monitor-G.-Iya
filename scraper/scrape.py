import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# =====================================
# CONFIG
# =====================================

URL = "https://magma.esdm.go.id/v1/gunung-api/laporan/search/q"

history_path = "../data/history.json"
latest_path = "../data/latest.json"

# =====================================
# DATE RANGE
# =====================================

end = datetime.now()
start = end - timedelta(days=7)

params = {
    "code": "IYA",
    "start": start.strftime("%Y-%m-%d"),
    "end": end.strftime("%Y-%m-%d")
}

# =====================================
# HEADERS
# =====================================

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Referer": "https://magma.esdm.go.id"
}

# =====================================
# REQUEST
# =====================================

print("REQUESTING DATA...")

try:

    res = requests.get(
        URL,
        params=params,
        headers=headers,
        timeout=30
    )

    print("STATUS:", res.status_code)

except Exception as e:

    print("REQUEST ERROR:", e)
    exit()

# =====================================
# SAVE DEBUG RESPONSE
# =====================================

with open("../data/debug.html", "w", encoding="utf-8") as f:
    f.write(res.text)

# =====================================
# PARSE RESPONSE
# =====================================

history_new = []

# coba parse JSON dulu
try:

    data = res.json()

    print("JSON DETECTED")

    items = []

    if isinstance(data, dict):
        items = data.get("data", [])

    elif isinstance(data, list):
        items = data

    for item in items:

        text = str(item)

        history_new.append({
            "date": item.get("tanggal")
                    or item.get("date")
                    or str(end.date()),

            "status": item.get("status")
                      or "UNKNOWN",

            "gempa": text.lower().count("gempa"),

            "raw": text[:500]
        })

except Exception:

    print("NOT JSON, TRY HTML PARSE")

    soup = BeautifulSoup(res.text, "html.parser")

    text = soup.get_text("\n")

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if len(line) < 15:
            continue

        if (
            "Level" in line
            or "WASPADA" in line
            or "SIAGA" in line
            or "NORMAL" in line
        ):

            history_new.append({
                "date": str(end.date()),
                "status": line,
                "gempa": line.lower().count("gempa"),
                "raw": line
            })

# =====================================
# FALLBACK
# =====================================

if len(history_new) == 0:

    print("NO DATA FOUND")

    history_new.append({
        "date": str(end.date()),
        "status": "DATA TIDAK TERBACA",
        "gempa": 0,
        "raw": res.text[:500]
    })

# =====================================
# LOAD OLD HISTORY
# =====================================

old_history = []

if os.path.exists(history_path):

    try:

        with open(history_path, "r", encoding="utf-8") as f:
            old_history = json.load(f)

    except Exception as e:

        print("ERROR LOAD OLD HISTORY:", e)
        old_history = []

# =====================================
# COMBINE DATA
# =====================================

combined = history_new + old_history

# remove duplicate berdasarkan tanggal
unique = {}

for item in combined:

    date_key = item.get("date", "")

    unique[date_key] = item

# final list
final_history = list(unique.values())

# urut terbaru
final_history.sort(
    key=lambda x: x.get("date", ""),
    reverse=True
)

# =====================================
# SAVE HISTORY
# =====================================

with open(history_path, "w", encoding="utf-8") as f:

    json.dump(
        final_history,
        f,
        indent=2,
        ensure_ascii=False
    )

# =====================================
# SAVE LATEST
# =====================================

latest = final_history[0]

with open(latest_path, "w", encoding="utf-8") as f:

    json.dump(
        latest,
        f,
        indent=2,
        ensure_ascii=False
    )

# =====================================
# DONE
# =====================================

print("SCRAPING DONE")
print("TOTAL DATA:", len(final_history))
