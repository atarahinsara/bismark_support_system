from app.models import Conversation
from app import db
from datetime import datetime

def get_open_conversation(sender_type, sender_id):
    """
    بررسی وجود مکالمه باز برای فرستنده بر اساس نوع و شناسه
    """
    if sender_type == "Customer":
        return Conversation.query.filter_by(CustomerID=sender_id, IsOpen=True).first()
    elif sender_type == "SalesRepresentative":
        return Conversation.query.filter_by(SalesRepID=sender_id, IsOpen=True).first()
    elif sender_type == "ServiceTechnician":
        return Conversation.query.filter_by(TechnicianID=sender_id, IsOpen=True).first()
    elif sender_type == "TempCustomer":
        return ConversationTemp.query.filter_by(TempCustomerID=sender_id, IsOpen=True).first()
    else:
        return None


def create_conversation(sender_type, sender_id):
    print(f"sender_type: {sender_type}, sender_id: {sender_id}")
    try:
        conv = Conversation(SenderID=sender_id, IsOpen=True, StartTime=datetime.utcnow())
        db.session.add(conv)
        db.session.commit()
        return conv
    except Exception as e:
        db.session.rollback()
        print(f"❌ خطا در ایجاد مکالمه: {e}")
        return None


