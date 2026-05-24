import requests
import json
import os
import re

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# =========================================
# CONFIG
# =========================================

URL = "https://magma.esdm.go.id/gunung-api/laporan"

history_path = "../data/history.json"

# =========================================
# DATE
# =========================================

end = datetime.now()
start = end - timedelta(days=7)

params = {
    "code": "IYA",
    "start_date": start.strftime("%Y-%m-%d"),
    "end_date": end.strftime("%Y-%m-%d")
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
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

html = res.text

# save debug
os.makedirs("../data", exist_ok=True)

with open("../data/debug.html", "w", encoding="utf-8") as f:
    f.write(html)

# =========================================
# PARSE HTML
# =========================================

soup = BeautifulSoup(html, "html.parser")

text = soup.get_text("\n")

# =========================================
# HELPERS
# =========================================

def extract(pattern, text):

    m = re.search(pattern, text, re.IGNORECASE)

    if m:
        return int(m.group(1))

    return 0

# =========================================
# DATE
# =========================================

today = datetime.now().strftime("%Y-%m-%d")

# =========================================
# DATA
# =========================================

parsed = {

    "date": today,

    "time": datetime.now().strftime("%H:%M"),

    "status": "LEVEL II",

    "gempa": {

        "vulkanik_dalam":
            extract(r'vulkanik dalam[^0-9]*(\d+)', text),

        "vulkanik_dangkal":
            extract(r'vulkanik dangkal[^0-9]*(\d+)', text),

        "low_frequency":
            extract(r'low freq[^0-9]*(\d+)', text),

        "tornillo":
            extract(r'tornillo[^0-9]*(\d+)', text),

        "hembusan":
            extract(r'hembusan[^0-9]*(\d+)', text),

        "tremor_harmonik":
            extract(r'tremor harmonik[^0-9]*(\d+)', text),

        "tremor_non_harmonik":
            extract(r'tremor non harmonik[^0-9]*(\d+)', text),

        "tremor_menerus":
            extract(
                r'tremor (?:menerus|terus menerus|kontinu)[^0-9]*(\d+)',
                text
            ),

        "tektonik_lokal":
            extract(r'tektonik lokal[^0-9]*(\d+)', text),

        "tektonik_jauh":
            extract(r'tektonik jauh[^0-9]*(\d+)', text),
    },

    "raw": text[:2000]
}

# =========================================
# LOAD OLD HISTORY
# =========================================

old_history = []

if os.path.exists(history_path):

    try:

        with open(history_path, "r", encoding="utf-8") as f:

            loaded = json.load(f)

            if isinstance(loaded, list):
                old_history = loaded

            elif isinstance(loaded, dict):
                old_history = [loaded]

    except Exception as e:

        print("LOAD ERROR:", e)

# =========================================
# COMBINE
# =========================================

combined = [parsed] + old_history

unique = {}

for item in combined:

    key = f"{item.get('date','')}_{item.get('time','')}"

    unique[key] = item

final_history = list(unique.values())

# newest first
final_history.sort(
    key=lambda x: f"{x.get('date','')} {x.get('time','')}",
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
print("TOTAL:", len(final_history))
