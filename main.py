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
def get_reasoning(english, arabic):
    match = df[
        (df["English text"].str.strip() == english.strip()) &
        (df["incorrect translation"].str.strip() == arabic.strip())
    ]
    if not match.empty:
        return match.iloc[0]["Reasoning for incorrect"]
    else:
        return "❌ لم يتم العثور على تحليل لهذه الجملة. تأكد من التطابق التام مع البيانات."

# نقطة النهاية للتحليل
@app.post("/analyze")
def analyze(req: TranslationRequest):
    reasoning = get_reasoning(req.english, req.arabic)
    return {"analysis": reasoning}
