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
