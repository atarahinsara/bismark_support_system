# app/nlp/nlp_utils.py

import re
from app.models.nlp.Nlp_Intents import NlpIntent
from app.nlp.ner_utils import extract_names_fa

def detect_intent(message_text):
    """
    بررسی intent با تطبیق مثال‌ها + بررسی نام با BERT
    """
    intents = NlpIntent.query.all()
    message_lower = message_text.lower().strip()
    print("🔍 در حال بررسی intent برای پیام:", message_lower)

    for intent in intents:
        if intent.Examples:
            examples = [ex.strip().lower() for ex in re.split(r'[،,]', intent.Examples)]
            print(f"➕ بررسی intent: {intent.Name} با نمونه‌ها: {examples}")

            for ex in examples:
                if ex in message_lower:
                    print(f"✅ Intent تشخیص داده شد: {intent.Name}")
                    return intent

    # Fallback: تشخیص نام با BERT
    detected_names = extract_names_fa(message_text)
    if detected_names:
        print(f"✅ نام/نام خانوادگی تشخیص داده شد: {detected_names}")
        return next((i for i in intents if i.Name == "ProvideName"), None)

    print("❌ هیچ Intentی مطابقت نداشت.")
    return None
