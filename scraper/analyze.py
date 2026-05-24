import json

# =========================================
# LOAD
# =========================================

with open('../data/history.json', 'r', encoding='utf-8') as f:
    history = json.load(f)

# =========================================
# VALIDATION
# =========================================

if not isinstance(history, list):

    history = [history]

# =========================================
# NOT ENOUGH DATA
# =========================================

if len(history) < 2:

    result = {
        "summary": "Data belum cukup untuk analisis tren aktivitas.",
        "warning": "Belum tersedia data pembanding.",
        "risk_score": 0
    }

else:

    latest = history[0]
    previous = history[1]

    latest_g = latest["gempa"]
    prev_g = previous["gempa"]

    analysis = []

    risk_score = 0

    # =====================================
    # Vulkanik Dangkal
    # =====================================

    if latest_g["vulkanik_dangkal"] > prev_g["vulkanik_dangkal"]:

        analysis.append(
            "Terjadi peningkatan gempa vulkanik dangkal dibanding hari sebelumnya. "
            "Pola ini dapat mengindikasikan adanya pergerakan magma menuju permukaan."
        )

        risk_score += 20

    # =====================================
    # Vulkanik Dalam
    # =====================================

    if latest_g["vulkanik_dalam"] > prev_g["vulkanik_dalam"]:

        analysis.append(
            "Gempa vulkanik dalam mengalami peningkatan yang dapat berkaitan "
            "dengan suplai magma dari kedalaman."
        )

        risk_score += 15

    # =====================================
    # Tremor Harmonik
    # =====================================

    if latest_g["tremor_harmonik"] > 0:

        analysis.append(
            "Kemunculan tremor harmonik menunjukkan adanya aktivitas fluida "
            "atau gas vulkanik yang bergerak kontinu."
        )

        risk_score += 15

    # =====================================
    # Tremor Menerus
    # =====================================

    if latest_g["tremor_menerus"] > 0:

        analysis.append(
            "Terdeteksi tremor menerus yang dapat mengindikasikan "
            "aktivitas internal gunung api masih berlangsung."
        )

        risk_score += 20

    # =====================================
    # Low Frequency
    # =====================================

    if latest_g["low_frequency"] > prev_g["low_frequency"]:

        analysis.append(
            "Gempa low frequency mengalami peningkatan dan sering "
            "dikaitkan dengan pergerakan fluida vulkanik."
        )

        risk_score += 10

    # =====================================
    # Tornillo
    # =====================================

    if latest_g["tornillo"] > 0:

        analysis.append(
            "Kemunculan gempa tornillo dapat berkaitan dengan tekanan gas "
            "atau resonansi fluida di dalam sistem vulkanik."
        )

        risk_score += 20

    # =====================================
    # FALLBACK
    # =====================================

    if len(analysis) == 0:

        analysis.append(
            "Belum terlihat perubahan signifikan pada pola kegempaan "
            "dibanding periode sebelumnya."
        )

    # =====================================
    # WARNING LEVEL
    # =====================================

    if risk_score >= 70:

        warning = "Aktivitas vulkanik tinggi. Pemantauan intensif diperlukan."

    elif risk_score >= 40:

        warning = "Terjadi peningkatan aktivitas vulkanik."

    else:

        warning = "Aktivitas vulkanik relatif stabil."

    # =====================================
    # RESULT
    # =====================================

    result = {

        "date": latest["date"],

        "time": latest.get("time", ""),

        "status": latest["status"],

        "risk_score": risk_score,

        "warning": warning,

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
