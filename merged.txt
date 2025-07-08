"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("پیام جدید دریافت شد:", data)
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
////////////////////
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# تنظیمات
TOKEN = "$2b$10$8sdQhP86c6QsfOCI3set4ugI2gadgnHB6KzD0MSIGt6Z5FGVlpRXO"
API_URL = "http://localhost:21465/api/mySession/send-message"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("پیام جدید دریافت شد:", data)

    # اگر رویداد پیام باشه
    if data.get("event") == "onmessage":
        sender = data.get("from")
        message = data.get("body")

        if sender and message:
            response_text = f"سلام ✨ پیام شما دریافت شد: {message}"
            
            payload = {
                "phone": sender.replace("@c.us", ""),
                "message": response_text
            }

            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }

            try:
                r = requests.post(API_URL, json=payload, headers=headers)
                print("✅ پاسخ ارسال شد:", r.status_code, r.text)
            except Exception as e:
                print("❌ خطا در ارسال پاسخ:", e)

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
