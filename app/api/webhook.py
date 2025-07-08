from flask import Blueprint, request, jsonify
from app import db
from app.api.helpers import (
    normalize_phone,
    detect_sender_with_welcome_status,
    build_response,
    process_conversation_flow,
    append_message_to_temp_customer,
    get_or_create_flow
)
from app.models.nlp.Annotation import MessageAnnotation

from app.api.wppconnect_api import send_message_to_user
from app.api.welcome import create_conversation
from app.models.nlp.Nlp_Intents import NLPIntent

#from app.models.NLP_Intents import NLPIntent
from app.nlp_training.entity_extractor import extract_entities_from_text  # فایلی که پایین می‌سازیم

import json

bp = Blueprint('webhook', __name__)

ALLOWED_NUMBERS = ["09192806966"]


@bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data.get("event") != "onmessage" or data.get("isGroupMsg") or data.get("fromMe"):
        return jsonify({"status": "ignored"}), 200

    raw_phone = data.get("from")
    message = data.get("body", "").strip()
    session_id = data.get("session")

    if not raw_phone:
        return jsonify({"error": "No sender phone"}), 400

    phone = normalize_phone(raw_phone)
    print(f"📥 پیام از: {phone} - متن: {message}")

    # فقط شماره‌های مجاز اجازه ادامه دارند
    if phone not in ALLOWED_NUMBERS:
        print(f"⚠️ شماره {phone} مجاز نیست.")
        return jsonify({"status": "number_not_allowed"}), 200

    # 🔍 تحلیل NLP: intent و entity
    predicted_intent = NLPIntent.query.filter_by(name='معرفی شخص').first()  # تستی - بعداً مدل جایگزین میشه
    entities = extract_entities_from_text(message)  # از فایل entity_extractor

    print(f"🤖 Intent: {predicted_intent.name if predicted_intent else 'نامشخص'}")
    print(f"📍 Entities: {entities}")

    annotation = MessageAnnotation(
        original_message=message,
        intent_id=predicted_intent.id if predicted_intent else None,
        entities=json.dumps(entities, ensure_ascii=False),
        annotated_by="system"
    )
    db.session.add(annotation)
    db.session.commit()

    # بررسی نقش فرستنده
    sender_type, sender_id, sender_obj, has_open_conv = detect_sender_with_welcome_status(phone)

    if not has_open_conv:
        create_conversation(sender_type, sender_id)
        welcome_msg = build_response(sender_type, phone)
        send_message_to_user(session_id, phone, welcome_msg)
        return jsonify({"status": "welcome_sent"})

    if sender_type == "TempCustomer":
        append_message_to_temp_customer(phone, message, entities)
        response_text = process_conversation_flow(phone, message)
        send_message_to_user(session_id, phone, response_text)
        return jsonify({"status": "flow_handled"})

    return jsonify({"status": "ignored"}), 200
