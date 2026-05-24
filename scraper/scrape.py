import requests
import json
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

URL = "https://magma.esdm.go.id/v1/gunung-api/laporan/search/q"

history_path = "../data/history.json"

end = datetime.now()
start = end - timedelta(days=7)

params = {
    "code": "IYA",
    "start": start.strftime("%Y-%m-%d"),
    "end": end.strftime("%Y-%m-%d")
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://magma.esdm.go.id"
}

res = requests.get(
    URL,
    params=params,
    headers=headers,
    timeout=30
)

print("STATUS:", res.status_code)

text = res.text

with open("../data/debug.html", "w", encoding="utf-8") as f:
    f.write(text)

# =========================================
# PARSE
# =========================================

def extract_number(pattern, text):

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        try:
            return int(match.group(1))
        except:
            return 0

    return 0

history_new = []

try:

    data = res.json()

    if isinstance(data, dict):
        items = data.get("data", [])
    else:
        items = data

    for item in items:

        raw = str(item)

        laporan = raw.lower()

        parsed = {
            "date": item.get("tanggal", ""),
            "status": item.get("status", "UNKNOWN"),

            "gempa": {
                "vulkanik_dalam":
                    extract_number(r'vulkanik dalam[^0-9]*(\d+)', laporan),

                "vulkanik_dangkal":
                    extract_number(r'vulkanik dangkal[^0-9]*(\d+)', laporan),

                "low_frequency":
                    extract_number(r'low freq[^0-9]*(\d+)', laporan),

                "tornillo":
                    extract_number(r'tornillo[^0-9]*(\d+)', laporan),

                "hembusan":
                    extract_number(r'hembusan[^0-9]*(\d+)', laporan),

                "tremor_harmonik":
                    extract_number(r'tremor harmonik[^0-9]*(\d+)', laporan),

                "tremor_non_harmonik":
                    extract_number(r'tremor non harmonik[^0-9]*(\d+)', laporan),

                "tremor_menerus":
                    extract_number(r'tremor terus menerus[^0-9]*(\d+)', laporan),

                "tektonik_lokal":
                    extract_number(r'tektonik lokal[^0-9]*(\d+)', laporan),

                "tektonik_jauh":
                    extract_number(r'tektonik jauh[^0-9]*(\d+)', laporan),
            },

            "raw": raw[:1000]
        }

        history_new.append(parsed)

except Exception as e:

    print("PARSE ERROR:", e)

# =========================================
# LOAD OLD HISTORY
# =========================================

old_history = []

if os.path.exists(history_path):

    with open(history_path, "r", encoding="utf-8") as f:
        try:
            old_history = json.load(f)
        except:
            old_history = []

# =========================================
# COMBINE
# =========================================

combined = history_new + old_history

unique = {}

for item in combined:

    date_key = item.get("date", "")

    unique[date_key] = item

final_history = list(unique.values())

final_history.sort(
    key=lambda x: x.get("date", ""),
    reverse=True
)

# =========================================
# SAVE
# =========================================

with open(history_path, "w", encoding="utf-8") as f:

    json.dump(
        final_history,
        f,
        indent=2,
        ensure_ascii=False
    )

print("SCRAPING DONE")
