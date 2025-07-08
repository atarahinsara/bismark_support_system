from app import db

class MessageAnnotation(db.Model):
    __tablename__ = 'message_annotations'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    intent_id = db.Column(db.Integer, db.ForeignKey('nlp_intents.id'))
    confidence = db.Column(db.Float)  # ضریب اطمینان مدل
    annotated_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    original_message = db.Column(db.Text)
    entities = db.Column(db.Text)  # فیلد جدید برای ذخیره‌سازی نهادهای استخراج شده (به صورت JSON string)

    # رابطه با intent (اختیاری، اگر خواستی دسترسی برعکس داشته باشی)
    intent = db.relationship("NLPIntent", backref=db.backref("annotations", lazy='dynamic'))
