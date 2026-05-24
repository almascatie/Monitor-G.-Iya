import json
import google.generativeai as genai
from config import GEMINI_API_KEY

with open('../data/history.json', 'r', encoding='utf-8') as f:
    history = json.load(f)

with open('../prompts/gemini_prompt.txt', 'r', encoding='utf-8') as f:
    prompt_base = f.read()

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

prompt = f"""
{prompt_base}

Data:
{json.dumps(history, indent=2, ensure_ascii=False)}
"""

response = model.generate_content(prompt)

summary = response.text

avg_gempa = sum([x['gempa'] for x in history]) / len(history)

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

with open('../data/analysis.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print('Analisis AI selesai')
