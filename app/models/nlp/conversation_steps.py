from app import db
from datetime import datetime

class NLPConversationStep(db.Model):
    __tablename__ = 'nlp_conversation_steps'

    StepID = db.Column(db.Integer, primary_key=True)
    StepKey = db.Column(db.String(50), nullable=False, unique=True)  # مثلاً: first_name
    PromptMessage = db.Column(db.Text, nullable=False)  # پیامی که به کاربر نمایش داده می‌شود
    FieldName = db.Column(db.String(50), nullable=False)  # نام فیلدی که باید در CustomerTemp ذخیره شود
    Order = db.Column(db.Integer, nullable=False, index=True)  # ترتیب نمایش مراحل
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
