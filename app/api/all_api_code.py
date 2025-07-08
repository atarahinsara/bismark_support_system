from app.models import Conversation, Customer

def has_open_conversation(customer_phone):
    """
    بررسی می‌کند که آیا مشتری با شماره داده شده، مکالمه باز (IsOpen=True) دارد یا خیر.

    ورودی:
        customer_phone (str): شماره تلفن مشتری به فرمت دیتابیس

    خروجی:
        bool: True اگر مکالمه باز وجود داشته باشد، False در غیر این صورت
    """
    customer = Customer.query.filter_by(phone=customer_phone).first()
    if not customer:
        return False

    open_conversation = Conversation.query.filter_by(CustomerID=customer.CustomerID, IsOpen=True).first()
    return open_conversation is not None
from app.models import (
    Customer, CustomerPhone,
    SalesRepresentativePhone,
    TechnicianPhone,
    MessageTemplate
)
from sqlalchemy.orm import joinedload

def normalize_phone(phone: str) -> str:
    """
    نرمال‌سازی شماره تلفن به فرمت 0XXXXXXXXXX
    حذف پسوند @c.us و تبدیل +98 یا 98 به 0
    """
    phone = phone.strip()
    if phone.endswith('@c.us'):
        phone = phone.replace('@c.us', '')
    if phone.startswith("+98"):
        return "0" + phone[3:]
    if phone.startswith("98"):
        return "0" + phone[2:]
    if phone.startswith("0"):
        return phone
    return phone


def detect_sender(phone: str):
    """
    تشخیص نوع فرستنده بر اساس شماره تلفن:
    مشتری، نماینده فروش، تکنسین یا ناشناس
    """
    # جستجو در مشتری‌ها
    customer = Customer.query \
        .join(CustomerPhone, Customer.CustomerID == CustomerPhone.CustomerID) \
        .options(joinedload(Customer.Phones)) \
        .filter(CustomerPhone.PhoneNumber == phone) \
        .first()
    if customer:
        return "Customer", customer.CustomerID, customer

    # جستجو در نماینده‌های فروش
    sales_rep_phone = SalesRepresentativePhone.query \
        .options(joinedload(SalesRepresentativePhone.SalesRepresentative)) \
        .filter(SalesRepresentativePhone.PhoneNumber == phone) \
        .first()
    if sales_rep_phone:
        return "SalesRepresentative", sales_rep_phone.SalesRepID, sales_rep_phone.SalesRepresentative

    # جستجو در تکنسین‌ها
    technician_phone = TechnicianPhone.query \
        .options(joinedload(TechnicianPhone.Technician)) \
        .filter(TechnicianPhone.PhoneNumber == phone) \
        .first()
    if technician_phone:
        return "ServiceTechnician", technician_phone.TechnicianID, technician_phone.Technician

    # در صورتی که یافت نشد
    return "Unknown", None, None


def build_response(sender_type: str, person, is_welcome=False) -> str:
    """
    ساخت متن پاسخ براساس نوع فرستنده و قالب پیام‌ها
    """
    if is_welcome:
        welcome_type = f"{sender_type}_Welcome"
        template_obj = MessageTemplate.query.filter_by(sender_type=welcome_type).first()
        if not template_obj:
            template_obj = MessageTemplate.query.filter_by(sender_type="Welcome_Default").first()
    else:
        template_obj = MessageTemplate.query.filter_by(sender_type=sender_type).first()

    if not template_obj:
        template_obj = MessageTemplate.query.filter_by(sender_type="Unknown").first()
        if not template_obj:
            return (
                "سلام 🙏 خوش آمدید به پشتیبانی واتساپ شرکت بیسمارک.\n"
                "شما در حال حاضر در سیستم ثبت نشده‌اید.\n"
                "لطفاً برای شروع، نام و نام خانوادگی خود را وارد نمایید."
            )

    name = f"{person.FirstName or ''} {person.LastName or ''}".strip() if person else ""
    city_info = getattr(person, "City", "") if person else ""
    gender_name = ""
    if person and getattr(person, "Gender", None):
        gender_name = getattr(person.Gender, "GenderName", "")

    # اصلاح sender_type به مقادیر صحیح که در دیتابیس استفاده می‌شود
    # اگر نام دقیق در دیتابیس متفاوت است این خط را متناسب تغییر بده
    gender_prefix = gender_name if sender_type in ["SalesRepresentative", "ServiceTechnician"] else ""

    response_text = template_obj.message_template.format(
        name=name,
        city_info=city_info,
        gender_prefix=gender_prefix
    )

    return response_text.strip()
from app.models import MessageTemplate

def build_response(sender_type, person, is_welcome=False):
    # اگر پیام خوش‌آمد باید داده شود، قالب مربوط را بگیر
    if is_welcome:
        # مثلا قالبی با sender_type ترکیبی مثل 'customer_Welcome'
        welcome_type = f"{sender_type}_Welcome"
        template_obj = MessageTemplate.query.filter_by(sender_type=welcome_type).first()
        if not template_obj:
            # اگر قالب خوش‌آمد موجود نبود، از قالب پیش‌فرض استفاده کن
            template_obj = MessageTemplate.query.filter_by(sender_type="Welcome_Default").first()
    else:
        template_obj = MessageTemplate.query.filter_by(sender_type=sender_type).first()

    if not template_obj:
        template_obj = MessageTemplate.query.filter_by(sender_type="Unknown").first()
        if not template_obj:
            return (
                "سلام 🙏 خوش آمدید به پشتیبانی واتساپ شرکت بیسمارک.\n"
                "شما در حال حاضر در سیستم ثبت نشده‌اید.\n"
                "لطفاً برای شروع، نام و نام خانوادگی خود را وارد نمایید."
            )

    name = f"{person.FirstName or ''} {person.LastName or ''}".strip() if person else ""
    city_info = getattr(person, "City", "") if person else ""
    gender_name = ""
    if person and getattr(person, "Gender", None):
        gender_name = getattr(person.Gender, "GenderName", "")

    gender_prefix = gender_name if sender_type in ["SalesRep", "Technician"] else ""

    response_text = template_obj.message_template.format(
        name=name,
        city_info=city_info,
        gender_prefix=gender_prefix
    )

    return response_text.strip()
from app.models import Customer, CustomerPhone, SalesRepresentativePhone, TechnicianPhone
from sqlalchemy.orm import joinedload

def detect_sender(phone):
    # جستجو در مشتری‌ها
    customer = Customer.query \
        .join(CustomerPhone, Customer.CustomerID == CustomerPhone.CustomerID) \
        .options(joinedload(Customer.Phones)) \
        .filter(CustomerPhone.PhoneNumber == phone) \
        .first()
    if customer:
        return "Customer", customer.CustomerID, customer

    # جستجو در نماینده‌های فروش
    sales_rep_phone = SalesRepresentativePhone.query \
        .options(joinedload(SalesRepresentativePhone.SalesRepresentative)) \
        .filter(SalesRepresentativePhone.PhoneNumber == phone) \
        .first()
    if sales_rep_phone:
        return "SalesRepresentative", sales_rep_phone.SalesRepID, sales_rep_phone.SalesRepresentative

    # جستجو در تکنسین‌ها
    technician_phone = TechnicianPhone.query \
        .options(joinedload(TechnicianPhone.Technician)) \
        .filter(TechnicianPhone.PhoneNumber == phone) \
        .first()
    if technician_phone:
        return "ServiceTechnician", technician_phone.TechnicianID, technician_phone.Technician

    # در صورتی که یافت نشد
    return "Unknown", None, None
from flask import Blueprint, request, jsonify
from app.utils.db_helpers import add_and_commit
from app.api.wppconnect_api import send_message
from app.api.helpers import detect_sender, build_response, normalize_phone
from app.models import Conversation, CustomerTemp, ConversationTemp
from app import db
from datetime import datetime

bp = Blueprint('webhook', __name__)

@bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # استخراج شماره فرستنده امن‌تر
    sender_phone_raw = None
    if 'id' in data and isinstance(data['id'], dict) and 'from' in data['id']:
        sender_phone_raw = data['id']['from']
    elif 'from' in data:
        sender_phone_raw = data['from']

    if not sender_phone_raw:
        return jsonify({"status": "error", "message": "شماره فرستنده پیدا نشد"}), 400

    sender_phone = normalize_phone(sender_phone_raw)
    print(f"📲 Detecting sender for phone: {sender_phone}")

    sender_type, sender_id, sender_obj = detect_sender(sender_phone)
    print(f"📌 فرستنده: {sender_phone} | نقش: {sender_type} | ID: {sender_id}")

    conversation = None
    conversation_temp = None

    # مدیریت مکالمات بر اساس نوع فرستنده
    if sender_type == "Customer" and sender_id:
        conversation = Conversation.get_open_by_customer(sender_id)
        if not conversation:
            conversation = Conversation.create_for_customer(sender_id)

    elif sender_type == "SalesRepresentative" and sender_id:
        conversation = Conversation.query.filter_by(SalesRepID=sender_id, IsOpen=True).first()
        if not conversation:
            conversation = Conversation(SalesRepID=sender_id, IsOpen=True)
            add_and_commit(conversation)

    elif sender_type == "ServiceTechnician" and sender_id:
        conversation = Conversation.query.filter_by(TechnicianID=sender_id, IsOpen=True).first()
        if not conversation:
            conversation = Conversation(TechnicianID=sender_id, IsOpen=True)
            add_and_commit(conversation)

    else:
        # ناشناس‌ها با مشتری موقت و کانورسیشن موقت مدیریت می‌شوند
        temp = CustomerTemp.query.filter_by(UserNumber=sender_phone, Status='collecting').first()
        if not temp:
            temp = CustomerTemp.create(user_number=sender_phone)

        conversation_temp = ConversationTemp.get_open_by_temp_customer(temp.TempID)
        if not conversation_temp:
            conversation_temp = ConversationTemp.create_for_temp_customer(temp.TempID)

    # ساخت پاسخ با توجه به نوع فرستنده و وضعیت

    if sender_type == "Customer" and sender_id is None:
        temp_customer = CustomerTemp.get_by_number(sender_phone)
        if temp_customer and not temp_customer.WelcomeSent:
            reply = (
                "سلام 🙏 خوش آمدید به پشتیبانی واتساپ شرکت بیسمارک.\n"
                "شما در حال حاضر در سیستم ثبت نشده‌اید.\n"
                "لطفاً برای شروع، نام و نام خانوادگی خود را وارد نمایید."
            )
            # پرچم پیام خوش‌آمد را True کن
            temp_customer.WelcomeSent = True
            db.session.commit()
        else:
            # اگر پیام قبلا ارسال شده، پیام دیگری یا هیچ پیامی نده
            reply = "پیام قبلا ارسال شده است."
    else:
        reply = build_response(sender_type, sender_obj)

    send_resp = send_message(sender_phone, reply)

    return jsonify({"status": "success", "response": send_resp})
# wppconnect_api.py
import requests
from flask import current_app

def to_api_phone_format(phone: str) -> str:
    """
    تبدیل شماره تلفن به فرمت API واتساپ WPPConnect:
    مثلا 09123456789 -> 989123456789
    """
    phone = phone.strip()
    if phone.startswith("0") and len(phone) == 11:
        return "98" + phone[1:]
    if phone.startswith("+98"):
        return phone[1:]
    if phone.startswith("98") and len(phone) == 12:
        return phone
    return phone

def send_message(phone: str, message: str) -> dict:
    """
    ارسال پیام به شماره مشخص شده از طریق API WPPConnect
    """
    api_phone = to_api_phone_format(phone)

    base_url = current_app.config.get('WPP_API_BASE_URL')
    session = current_app.config.get('WPP_SESSION_NAME')
    token = current_app.config.get('WPP_SESSION_TOKEN')

    url = f"{base_url}/{session}/send-message"  # توکن حذف شده از URL

    payload = {
        "phone": api_phone,
        "message": message
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"📨 ارسال پیام: {response.status_code} {response.text}")
        try:
            return response.json()
        except Exception as e:
            print(f"⚠️ JSON decode error: {e}")
            return {"status": "error", "message": "Invalid JSON response"}
    except Exception as e:
        print(f"❌ خطای ارسال: {e}")
        return {"status": "error", "message": str(e)}
