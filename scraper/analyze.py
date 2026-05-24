import json

with open('../data/history.json', 'r', encoding='utf-8') as f:
    history = json.load(f)

if len(history) < 2:

    result = {
        "summary": "Data belum cukup untuk analisis tren aktivitas."
    }

else:

    latest = history[0]
    previous = history[1]

    latest_g = latest["gempa"]
    prev_g = previous["gempa"]

    analysis = []

    # =====================================
    # Vulkanik Dangkal
    # =====================================

    if latest_g["vulkanik_dangkal"] > prev_g["vulkanik_dangkal"]:

        analysis.append(
            "Terjadi peningkatan gempa vulkanik dangkal dibanding hari sebelumnya. "
            "Pola ini dapat mengindikasikan adanya pergerakan magma yang mulai "
            "mendekati permukaan."
        )

    # =====================================
    # Vulkanik Dalam
    # =====================================

    if latest_g["vulkanik_dalam"] > prev_g["vulkanik_dalam"]:

        analysis.append(
            "Gempa vulkanik dalam mengalami peningkatan. "
            "Hal ini dapat berkaitan dengan suplai magma dari kedalaman."
        )

    # =====================================
    # Tremor Harmonik
    # =====================================

    if latest_g["tremor_harmonik"] > 0:

        analysis.append(
            "Kemunculan tremor harmonik menunjukkan adanya aktivitas fluida "
            "atau gas vulkanik yang bergerak secara kontinu."
        )

    # =====================================
    # Tremor Menerus
    # =====================================

    if latest_g["tremor_menerus"] > 0:

        analysis.append(
            "Terdeteksi tremor terus menerus yang dapat mengindikasikan "
            "aktivitas internal gunung api masih berlangsung."
        )

    # =====================================
    # Low Frequency
    # =====================================

    if latest_g["low_frequency"] > prev_g["low_frequency"]:

        analysis.append(
            "Gempa low frequency mengalami peningkatan dibanding periode sebelumnya. "
            "Jenis gempa ini sering dikaitkan dengan pergerakan fluida vulkanik."
        )

    # =====================================
    # Tornillo
    # =====================================

    if latest_g["tornillo"] > 0:

        analysis.append(
            "Kemunculan gempa tornillo dapat berkaitan dengan tekanan gas "
            "atau resonansi fluida di dalam sistem vulkanik."
        )

    # =====================================
    # Fallback
    # =====================================

    if len(analysis) == 0:

        analysis.append(
            "Belum terlihat perubahan signifikan pada pola kegempaan vulkanik "
            "dibanding periode sebelumnya."
        )

    result = {
        "date": latest["date"],
        "status": latest["status"],
        "summary": "\n\n".join(analysis)
    }

# =====================================
# SAVE
# =====================================

with open('../data/analysis.json', 'w', encoding='utf-8') as f:

    json.dump(
        result,
        f,
        indent=2,
        ensure_ascii=False
    )

print("ANALYSIS DONE")
