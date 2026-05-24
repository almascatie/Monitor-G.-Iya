import json

# load history
with open('../data/history.json', 'r', encoding='utf-8') as f:
    history = json.load(f)

# ambil data gempa
gempa_values = [x.get('gempa', 0) for x in history]

if len(gempa_values) == 0:
    avg_gempa = 0
else:
    avg_gempa = sum(gempa_values) / len(gempa_values)

# risk score sederhana
risk_score = min(int(avg_gempa * 5), 100)

# level
if risk_score < 40:
    risk_level = "rendah"

    summary = (
        "Aktivitas vulkanik cenderung stabil "
        "dan belum menunjukkan peningkatan signifikan."
    )

elif risk_score < 70:
    risk_level = "sedang"

    summary = (
        "Terjadi peningkatan aktivitas ringan "
        "dibanding beberapa hari sebelumnya."
    )

else:
    risk_level = "tinggi"

    summary = (
        "Aktivitas vulkanik relatif tinggi "
        "dan perlu pemantauan lebih lanjut."
    )

result = {
    "risk_score": risk_score,
    "risk_level": risk_level,
    "summary": summary
}

# simpan hasil
with open('../data/analysis.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("ANALYSIS DONE")
