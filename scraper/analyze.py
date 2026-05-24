import json
import os
import google.generativeai as genai

# ambil API key dari GitHub Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# load data history
with open('../data/history.json', 'r', encoding='utf-8') as f:
    history = json.load(f)

# prompt dasar
with open('../prompts/gemini_prompt.txt', 'r', encoding='utf-8') as f:
    prompt_base = f.read()

model = genai.GenerativeModel('gemini-2.0-flash')
prompt = f"""
{prompt_base}

DATA:
{json.dumps(history, indent=2, ensure_ascii=False)}
"""

response = model.generate_content(prompt)

summary = response.text

# hitung risk score sederhana
if len(history) == 0:
    avg_gempa = 0
else:
    avg_gempa = sum([x.get('gempa', 0) for x in history]) / len(history)

risk_score = min(int(avg_gempa * 5), 100)

if risk_score < 40:
    risk_level = "rendah"
elif risk_score < 70:
    risk_level = "sedang"
else:
    risk_level = "tinggi"

result = {
    "risk_score": risk_score,
    "risk_level": risk_level,
    "summary": summary
}

# simpan hasil analisis
with open('../data/analysis.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("Analisis selesai")
