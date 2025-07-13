from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

# تحميل ملف الإكسل (مرة وحدة عند بدء التطبيق)
df = pd.read_excel("Final_Expanded_Examples.xlsx")

# تعريف API
app = FastAPI()

# نموذج البيانات
class TranslationRequest(BaseModel):
    english: str
    arabic: str

# دالة البحث في الملف
def get_analysis(english, arabic):
    match = df[
        (df["English text"].str.strip() == english.strip()) &
        (df["incorrect translation"].str.strip() == arabic.strip())
    ]
    if not match.empty:
        reasoning = match.iloc[0]["Reasoning for incorrect"]
        precise = match.iloc[0]["Precise Arabic translations"]
        return reasoning, precise
    else:
        return None, None

# نقطة النهاية للتحليل
@app.post("/analyze")
def analyze(req: TranslationRequest):
    reasoning, precise = get_analysis(req.english, req.arabic)
    if reasoning:
        return {
            "reasoning": reasoning,
            "precise_translation": precise
        }
    else:
        return {
            "reasoning": "❌ لم يتم العثور على تحليل.",
            "precise_translation": "—"
        }

