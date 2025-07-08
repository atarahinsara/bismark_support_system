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
    از session پیش‌فرض (از کانفیگ) استفاده می‌کند
    """
    api_phone = to_api_phone_format(phone)

    base_url = current_app.config.get('WPP_API_BASE_URL')
    session = current_app.config.get('WPP_SESSION_NAME')
    token = current_app.config.get('WPP_SESSION_TOKEN')

    url = f"{base_url}/{session}/send-message"

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
        #print(f"📨 ارسال پیام: {response.status_code} {response.text}")
        return response.json()
    except Exception as e:
        print(f"❌ خطای ارسال: {e}")
        return {"status": "error", "message": str(e)}


def send_message_to_user(session_id: str, phone: str, message: str) -> dict:
    """
    ارسال پیام به شماره مشخص شده از طریق API WPPConnect
    با مشخص کردن session_id داینامیک (غیر از session پیش‌فرض)
    """
    api_phone = to_api_phone_format(phone)

    base_url = current_app.config.get('WPP_API_BASE_URL')
    token = current_app.config.get('WPP_SESSION_TOKEN')

    url = f"{base_url}/{session_id}/send-message"

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
        #print(f"📨 ارسال پیام به session {session_id}: {response.status_code} {response.text}")
        return response.json()
    except Exception as e:
        print(f"❌ خطای ارسال به session {session_id}: {e}")
        return {"status": "error", "message": str(e)}
