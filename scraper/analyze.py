import json

data = json.load(open("../data/history.json"))

if len(data) < 2:
    result = {"summary": "Data belum cukup."}

else:

    latest = data[0]
    prev = data[1]

    g1 = latest["gempa"]
    g0 = prev["gempa"]

    notes = []

    def check(name, label):
        if g1[name] > g0[name]:
            notes.append(f"Peningkatan {label} dibanding hari sebelumnya.")

    check("vulkanik_dalam", "gempa vulkanik dalam")
    check("vulkanik_dangkal", "gempa vulkanik dangkal")
    check("low_frequency", "low frequency")
    check("tremor_harmonik", "tremor harmonik")
    check("tremor_menerus", "tremor terus menerus")

    if g1["tremor_harmonik"] > 0 or g1["tremor_menerus"] > 0:
        notes.append("Terjadi indikasi aktivitas fluida magmatik.")

    # WARNING LOGIC (tanpa angka)
    if g1["vulkanik_dangkal"] > g0["vulkanik_dangkal"] and g1["low_frequency"] > 0:
        warning = "PERHATIAN: pola menunjukkan peningkatan aktivitas magma dangkal."
    else:
        warning = "Tidak ada indikasi perubahan signifikan."

    if not notes:
        notes.append("Tidak ada perubahan signifikan pada pola kegempaan.")

    result = {
        "date": latest["date"],
        "time": latest["time"],
        "status": latest["status"],
        "warning": warning,
        "summary": "\n".join(notes)
    }

json.dump(result, open("../data/analysis.json", "w"), indent=2)

print("ANALYSIS DONE")
