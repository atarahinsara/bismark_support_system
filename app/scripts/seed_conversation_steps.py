from app import db
from app.models.nlp.conversation_steps import NLPConversationStep

steps = [
    {"StepKey": "first_name", "PromptMessage": "لطفاً نام خود را وارد کنید.", "FieldName": "first_name", "Order": 1},
    {"StepKey": "last_name", "PromptMessage": "عالیه، حالا نام خانوادگی‌تون؟", "FieldName": "last_name", "Order": 2},
    {"StepKey": "province", "PromptMessage": "استان محل سکونتتون رو وارد کنید.", "FieldName": "Province", "Order": 3},
    {"StepKey": "city", "PromptMessage": "نام شهرتون چیه؟", "FieldName": "City", "Order": 4},
    {"StepKey": "address", "PromptMessage": "خیلی خوب 😊 لطفاً آدرس کامل رو وارد کنید.", "FieldName": "Address", "Order": 5},
]

for s in steps:
    step = NLPConversationStep(**s)
    db.session.add(step)

db.session.commit()
print("✅ مراحل گفتگو با موفقیت ثبت شدند.")
