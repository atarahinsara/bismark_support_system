from app import db
from app.models import Customer, CustomerPhone,SalesRepresentative, SalesRepresentativePhone,ServiceTechnician, TechnicianPhone, CustomerTemp, MessageTemplate, Conversation, ConversationFlow
from app.models.nlp.conversation_steps import NLPConversationStep
from datetime import datetime
import json

from app.nlp.intent_recognition import detect_intent


def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    if phone.endswith('@c.us'):
        phone = phone.replace('@c.us', '')
    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    elif phone.startswith("98"):
        phone = "0" + phone[2:]
    return phone

# ============================
# بخش 2: شناسایی نقش و وضعیت مکالمه
# ============================
def detect_sender_with_welcome_status(phone: str):
    print(f"🔍 شناسایی فرستنده برای شماره: {phone}")

    customer = Customer.query.join(CustomerPhone).filter(CustomerPhone.PhoneNumber == phone).first()
    if customer:
        print(f"✅ فرستنده یک مشتری دائمی است: {customer.CustomerID}")
        open_conv = Conversation.query.filter_by(SenderID=customer.CustomerID, IsOpen=True).first()
        print(f"📂 مکالمه باز برای مشتری وجود دارد: {bool(open_conv)}")
        return "Customer", customer.CustomerID, customer, bool(open_conv)

    sales_rep = SalesRepresentative.query.join(SalesRepresentativePhone).filter(SalesRepresentativePhone.PhoneNumber == phone).first()
    if sales_rep:
        print(f"✅ فرستنده نماینده فروش است: {sales_rep.SalesRepID}")
        open_conv = Conversation.query.filter_by(SenderID=sales_rep.SalesRepID, IsOpen=True).first()
        print(f"📂 مکالمه باز برای نماینده فروش وجود دارد: {bool(open_conv)}")
        return "SalesRepresentative", sales_rep.SalesRepID, sales_rep, bool(open_conv)

    technician = ServiceTechnician.query.join(TechnicianPhone).filter(TechnicianPhone.PhoneNumber == phone).first()
    if technician:
        print(f"✅ فرستنده تکنسین خدمات است: {technician.TechnicianID}")
        open_conv = Conversation.query.filter_by(SenderID=technician.TechnicianID, IsOpen=True).first()
        print(f"📂 مکالمه باز برای تکنسین وجود دارد: {bool(open_conv)}")
        return "ServiceTechnician", technician.TechnicianID, technician, bool(open_conv)

    temp_customer = CustomerTemp.query.filter_by(PhoneNumber=phone).first()
    if temp_customer:
        print(f"✅ فرستنده مشتری موقت است: {temp_customer.TempID}")
        open_conv = Conversation.query.filter_by(SenderID=temp_customer.TempID, IsOpen=True).first()
        print(f"📂 مکالمه باز برای مشتری موقت وجود دارد: {bool(open_conv)}")
        return "TempCustomer", temp_customer.TempID, temp_customer, bool(open_conv)

from sqlalchemy.orm import joinedload

def build_response(sender_type: str, phone_number: str) -> str:
    print(f"📝 ساخت پیام پاسخ برای نوع فرستنده '{sender_type}' و شماره '{phone_number}'")
    person = None
    try:
        if sender_type == "Customer":
            person = Customer.query.join(CustomerPhone).filter(CustomerPhone.PhoneNumber == phone_number).options(joinedload(Customer.Gender)).first()
        elif sender_type == "SalesRepresentative":
            person = SalesRepresentative.query.join(SalesRepresentativePhone).filter(SalesRepresentativePhone.PhoneNumber == phone_number).options(joinedload(SalesRepresentative.Gender)).first()
        elif sender_type == "ServiceTechnician":
            person = ServiceTechnician.query.join(TechnicianPhone).filter(TechnicianPhone.PhoneNumber == phone_number).options(joinedload(ServiceTechnician.Gender)).first()
        elif sender_type == "TempCustomer":
            person = CustomerTemp.query.filter_by(PhoneNumber=phone_number).first()
    except Exception as e:
        print(f"❌ خطا در واکشی اطلاعات شخص: {e}")
        person = None



def get_or_create_flow(phone_number):
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
    for ent in entities:
        if ent.get('entity') == field_name:
            return ent.get('value')
    return None


def promote_to_customer(phone_number):
    temp = CustomerTemp.query.filter_by(PhoneNumber=phone_number).first()
    if not temp:
        raise Exception("مشتری موقت پیدا نشد!")

    customer = Customer(
        FirstName=temp.first_name or "",
        LastName=temp.last_name or "",
        Province=temp.Province or "",
        City=temp.City or "",
        Address=temp.Address or "",
        GenderID=None  # چون در مدل CustomerTemp فیلدی برای GenderID نیست، باید مقدار پیش‌فرض یا None بگذاریم
    )
    db.session.add(customer)
    db.session.commit()

    phone = CustomerPhone(
        CustomerID=customer.CustomerID,
        PhoneNumber=phone_number,
        PhoneType="Mobile"
    )
    db.session.add(phone)

    db.session.delete(temp)
    db.session.commit()


def process_conversation_flow(phone_number, message_text, entities=[]):
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

    if current_step.FieldName in temp_data:
        value_for_field = temp_data[current_step.FieldName]
    else:
        entity_value = get_value_from_entities(entities, current_step.FieldName)
        if entity_value:
            value_for_field = entity_value
        else:
            value_for_field = None

    if value_for_field is None or value_for_field == "":
        return current_step.PromptMessage

    temp_data[current_step.FieldName] = value_for_field
    print(f"✍️ مقدار دریافت شده برای فیلد '{current_step.FieldName}': {value_for_field}")

    next_step = NLPConversationStep.query.filter(NLPConversationStep.Order > current_step.Order)\
        .order_by(NLPConversationStep.Order.asc()).first()

    if next_step:
        flow.Step = next_step.StepKey
        response = next_step.PromptMessage
        print(f"➡️ حرکت به مرحله بعد: {next_step.StepKey}")
    else:
        print("🏁 رسیدن به انتهای مراحل، ارتقاء مشتری...")
        try:
            promote_to_customer(phone_number)
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
