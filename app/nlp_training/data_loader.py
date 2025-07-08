from app import db
from app.models import MessageAnnotation
import json

def load_annotations():
    # بارگذاری تمام داده‌های آنوتیشن شده از دیتابیس
    annotations = MessageAnnotation.query.all()
    data = []
    for ann in annotations:
        entities = json.loads(ann.entities) if ann.entities else []
        data.append({
            "text": ann.original_message,
            "intent_id": ann.intent_id,
            "entities": entities
        })
    return data
