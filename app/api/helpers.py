from app import db
from app.models import Customer, CustomerPhone, CustomerTemp, MessageTemplate, Conversation, ConversationFlow
from app.models.nlp.conversation_steps import NLPConversationStep
from datetime import datetime
import json

# اگر می‌خوای تشخیص intent اضافه کنی
from app.nlp.intent_recognition import detect_intent


def normalize_phone(phone: str) -> str:
    """
    نرمال‌سازی شماره تلفن: حذف پسوند واتساپ، تبدیل پیش‌شماره ایران به 0 شروع
    """
    phone = phone.strip()
    if phone.endswith('@c.us'):
        phone = phone.replace('@c.us', '')
    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    elif phone.startswith("98"):
        phone = "0" + phone[2:]
    return phone


def detect_sender_with_welcome_status(phone: str):
    """
    شناسایی فرستنده بر اساس شماره تلفن در جدول CustomerTemp
    اگر یافت نشد، رکورد جدید ایجاد می‌کند
    بررسی وجود مکالمه باز برای فرستنده
    """
    temp = CustomerTemp.query.filter_by(PhoneNumber=phone).first()
    if temp:
        open_conv = Conversation.query.filter_by(SenderID=temp.TempID, IsOpen=True).first()
        return "TempCustomer", temp.TempID, temp, bool(open_conv)

    new_temp = CustomerTemp(
        first_name="",
        last_name="",
        PhoneNumber=phone,
        Status="collecting",
        CreatedAt=datetime.utcnow()
    )
    db.session.add(new_temp)
    db.session.commit()
    return "TempCustomer", new_temp.TempID, new_temp, False


def build_response(sender_type: str, phone_number: str) -> str:
    template = MessageTemplate.query.filter_by(sender_type=sender_type).first()
    if not template:
        print(f"⚠️ قالب پیام خوش‌آمد برای نوع {sender_type} یافت نشد.")
    return template.message_template if template else "سلام 🙏 لطفاً نام و نام خانوادگی خود را وارد نمایید."
    return text


def get_or_create_flow(phone_number):
    """
    واکشی جریان مکالمه (ConversationFlow) یا ایجاد یک جریان جدید از اولین مرحله
    """
    flow = ConversationFlow.query.filter_by(PhoneNumber=phone_number).first()
    
    if not flow:
        first_step = NLPConversationStep.query.order_by(NLPConversationStep.Order.asc()).first()
        
        if not first_step:
            raise Exception("❌ هیچ مرحله‌ای در جدول NLPConversationStep وجود ندارد.")
        
        flow = ConversationFlow(
            PhoneNumber=phone_number,
            Step=first_step.StepKey,
            TempData=json.dumps({}),
            LastUpdated=datetime.utcnow()
        )
        db.session.add(flow)
        db.session.commit()

    return flow

def get_value_from_entities(entities, field_name):
    """
    جستجو و استخراج مقدار مرتبط با فیلد جاری از لیست entities
    """
    for ent in entities:
        if ent.get('entity') == field_name:
            return ent.get('value')
    return None


def process_conversation_flow(phone_number, message_text, entities=[]):
    """
    مدیریت جریان مکالمه:
    - تشخیص intent و پاسخ خداحافظی (اختیاری)
    - به روز رسانی داده های موقت براساس فیلد جاری و entity استخراج شده
    - حرکت به مرحله بعدی یا ارتقاء مشتری
    """
    intent, score = detect_intent(message_text)
    if intent:
        print(f"🔍 Intent detected: {intent} with confidence {score}")
        if intent == "خداحافظی":
            return "خداحافظ! اگر سوالی داشتی من اینجا هستم."

    flow = get_or_create_flow(phone_number)
    temp_data = json.loads(flow.TempData or '{}')

    print(f"🟢 مرحله فعلی: {flow.Step}")
    current_step = NLPConversationStep.query.filter_by(StepKey=flow.Step).first()
    if not current_step:
        print("⚠️ مرحله فعلی پیدا نشد!")
        return "⛔️ مشکلی در جریان گفتگو پیش آمد."

    # فقط اگر فیلد قبلاً ذخیره نشده بود، مقدار جدید ثبت شود
    if current_step.FieldName in temp_data:
        value_for_field = temp_data[current_step.FieldName]
    else:
        entity_value = get_value_from_entities(entities, current_step.FieldName)
        if entity_value:
            value_for_field = entity_value
        else:
            value_for_field = None

    if value_for_field is None or value_for_field == "":
        # مقدار فیلد خالیه؛ پیام برای اون مرحله دریافت نشده
        # پس مجدداً همان پیام درخواست آن مرحله را می‌دهیم
        return current_step.PromptMessage

    # به‌روزرسانی داده‌ها
    temp_data[current_step.FieldName] = value_for_field
    print(f"✍️ مقدار دریافت شده برای فیلد '{current_step.FieldName}': {value_for_field}")

    # مرحله بعدی
    next_step = NLPConversationStep.query.filter(NLPConversationStep.Order > current_step.Order)\
        .order_by(NLPConversationStep.Order.asc()).first()

    if next_step:
        flow.Step = next_step.StepKey
        response = next_step.PromptMessage
        print(f"➡️ حرکت به مرحله بعد: {next_step.StepKey}")
    else:
        print("🏁 رسیدن به انتهای مراحل، ارتقاء مشتری...")
        try:
            promote_to_customer(phone_number, temp_data)
            db.session.delete(flow)
            db.session.commit()
            print("✅ ارتقاء مشتری موفقیت‌آمیز بود و جریان حذف شد.")
            return "✅ اطلاعات شما ثبت شد. چطور می‌تونیم کمک‌تون کنیم؟ 😊"
        except Exception as e:
            print(f"❌ خطا در ارتقاء مشتری: {e}")
            return "⚠️ خطایی در ثبت اطلاعات رخ داد."

    flow.TempData = json.dumps(temp_data, ensure_ascii=False)
    flow.LastUpdated = datetime.utcnow()
    db.session.commit()

    return response


def promote_to_customer(phone_number, temp_data):
    """
    تبدیل مشتری موقت به مشتری دائم با انتقال اطلاعات و حذف داده‌های موقت
    """
    customer = Customer(
        FirstName=temp_data.get("first_name", ""),
        LastName=temp_data.get("last_name", ""),
        Province=temp_data.get("province", ""),
        City=temp_data.get("city", ""),
        Address=temp_data.get("address", ""),
        GenderID=temp_data.get("gender_id")
    )
    db.session.add(customer)
    db.session.commit()

    phone = CustomerPhone(
        CustomerID=customer.CustomerID,
        PhoneNumber=phone_number,
        PhoneType="Mobile"
    )
    db.session.add(phone)

    temp = CustomerTemp.query.filter_by(PhoneNumber=phone_number).first()
    if temp:
        db.session.delete(temp)

    db.session.commit()


def append_message_to_temp_customer(phone_number, new_message, entities):
    temp = CustomerTemp.query.filter_by(PhoneNumber=phone_number).first()
    if not temp:
        return

    flow = get_or_create_flow(phone_number)
    current_step_obj = NLPConversationStep.query.filter_by(StepKey=flow.Step).first()
    if not current_step_obj:
        print("⚠️ مرحله جاری در جدول NLPConversationStep یافت نشد.")
        return

    steps_order = [s.StepKey for s in NLPConversationStep.query.order_by(NLPConversationStep.Order.asc()).all()]
    current_index = steps_order.index(flow.Step) if flow.Step in steps_order else -1
    max_index = current_index

    # نگاشت entity به فیلد مدل
    entity_to_model_field = {
        "first_name": "first_name",
        "last_name": "last_name",
        "province": "Province",
        "city": "City",
        "address": "Address"
    }

    updated_fields = []

    for entity in entities:
        key = entity.get("entity")
        val = entity.get("value")
        model_field = entity_to_model_field.get(key)
        if model_field and hasattr(temp, model_field):
            setattr(temp, model_field, val)
            updated_fields.append(model_field)

            if model_field in steps_order:
                step_idx = steps_order.index(model_field)
                if step_idx > max_index:
                    max_index = step_idx

    if not updated_fields:
        print(f"⚠️ هیچ entity مرتبط با مرحله فعلی '{flow.Step}' یافت نشد. مقدار ذخیره نشد.")
        db.session.commit()
        return
    else:
        print(f"🔄 آپدیت TempCustomer - شماره: {phone_number} - فیلدها: {updated_fields}")

    if updated_fields:
        if max_index + 1 < len(steps_order):
            flow.Step = steps_order[max_index + 1]
            print(f"➡️ حرکت مرحله به: {flow.Step}")
        else:
            print("🏁 همه مراحل تکمیل شده")

    db.session.commit()
