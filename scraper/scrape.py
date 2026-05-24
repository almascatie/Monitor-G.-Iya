import requests
import json
import os
import re

from datetime import datetime, timedelta

# =========================================
# CONFIG
# =========================================

URL = "https://magma.esdm.go.id/v1/gunung-api/laporan/search/q"

history_path = "../data/history.json"

# =========================================
# DATE RANGE
# =========================================

end = datetime.now()
start = end - timedelta(days=7)

params = {
    "code": "IYA",
    "start": start.strftime("%Y-%m-%d"),
    "end": end.strftime("%Y-%m-%d")
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://magma.esdm.go.id/",
    "Origin": "https://magma.esdm.go.id"
}

# =========================================
# REQUEST
# =========================================

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
    exit(1)

text = res.text

# debug html
os.makedirs("../data", exist_ok=True)

with open("../data/debug.html", "w", encoding="utf-8") as f:
    f.write(text)

# =========================================
# HELPER
# =========================================

def extract_number(pattern, text):

    match = re.search(pattern, text, re.IGNORECASE)

    if match:

        try:
            return int(match.group(1))

        except:
            return 0

    return 0

# =========================================
# PARSE JSON
# =========================================

history_new = []

try:

    data = res.json()

except Exception as e:

    print("JSON PARSE ERROR:", e)

    print("RESPONSE:")
    print(text[:500])

    data = []

# =========================================
# EXTRACT DATA
# =========================================

try:

    if isinstance(data, dict):
        items = data.get("data", [])

    elif isinstance(data, list):
        items = data

    else:
        items = []

    for item in items:

        laporan = json.dumps(item).lower()

        parsed = {

            "date": item.get("tanggal", ""),

            "time": item.get("jam", ""),

            "status": item.get("status", "UNKNOWN"),

            "gempa": {

                "vulkanik_dalam":
                    extract_number(
                        r'vulkanik dalam[^0-9]*(\d+)',
                        laporan
                    ),

                "vulkanik_dangkal":
                    extract_number(
                        r'vulkanik dangkal[^0-9]*(\d+)',
                        laporan
                    ),

                "low_frequency":
                    extract_number(
                        r'low freq[^0-9]*(\d+)',
                        laporan
                    ),

                "tornillo":
                    extract_number(
                        r'tornillo[^0-9]*(\d+)',
                        laporan
                    ),

                "hembusan":
                    extract_number(
                        r'hembusan[^0-9]*(\d+)',
                        laporan
                    ),

                "tremor_harmonik":
                    extract_number(
                        r'tremor harmonik[^0-9]*(\d+)',
                        laporan
                    ),

                "tremor_non_harmonik":
                    extract_number(
                        r'tremor non harmonik[^0-9]*(\d+)',
                        laporan
                    ),

                "tremor_menerus":
                    extract_number(
                        r'tremor (?:terus menerus|menerus|kontinu)[^0-9]*(\d+)',
                        laporan
                    ),

                "tektonik_lokal":
                    extract_number(
                        r'tektonik lokal[^0-9]*(\d+)',
                        laporan
                    ),

                "tektonik_jauh":
                    extract_number(
                        r'tektonik jauh[^0-9]*(\d+)',
                        laporan
                    ),
            },

            "raw": laporan[:1000]
        }

        history_new.append(parsed)

except Exception as e:

    print("PARSE ERROR:", e)

# =========================================
# VALIDATE SCRAPE
# =========================================

if len(history_new) == 0:

    print("NO DATA PARSED")
    exit(1)

# =========================================
# LOAD OLD HISTORY
# =========================================

old_history = []

if os.path.exists(history_path):

    with open(history_path, "r", encoding="utf-8") as f:

        try:

            loaded = json.load(f)

            # kalau list
            if isinstance(loaded, list):
                old_history = loaded

            # kalau object lama
            elif isinstance(loaded, dict):
                old_history = [loaded]

            else:
                old_history = []

        except Exception as e:

            print("LOAD HISTORY ERROR:", e)

            old_history = []

# =========================================
# COMBINE
# =========================================

combined = history_new + old_history

unique = {}

for item in combined:

    key = f"{item.get('date','')}_{item.get('time','')}"

    unique[key] = item

final_history = list(unique.values())

# sort terbaru
final_history.sort(
    key=lambda x: f"{x.get('date','')} {x.get('time','')}",
    reverse=True
)

# =========================================
# SAVE
# =========================================

if len(final_history) == 0:

    print("FINAL HISTORY EMPTY")
    exit(1)

with open(history_path, "w", encoding="utf-8") as f:

    json.dump(
        final_history,
        f,
        indent=2,
        ensure_ascii=False
    )

print("SCRAPING DONE")
print("TOTAL DATA:", len(final_history))
