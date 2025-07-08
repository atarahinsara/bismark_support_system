from app import db
from datetime import datetime

class Conversation(db.Model):
    __tablename__ = 'conversations'

    ConversationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SenderID = db.Column(db.Integer, nullable=False)  # شناسه فرستنده (مشتری یا نماینده یا تکنسین)
    StartTime = db.Column(db.DateTime, default=datetime.utcnow)
    EndTime = db.Column(db.DateTime, nullable=True)
    IsOpen = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Conversations {self.ConversationID} SenderID={self.SenderID} IsOpen={self.IsOpen}>"

# =====================
# متدهای CRUD برای Conversations
# =====================

def create_conversation(sender_id: int):
    conversation = Conversation(SenderID=sender_id)
    db.session.add(conversation)
    db.session.commit()
    return conversation


def get_conversation_by_id(conversation_id: int):
    return Conversation.query.get(conversation_id)


def get_open_conversation_by_sender(sender_id: int):
    return Conversation.query.filter_by(SenderID=sender_id, IsOpen=True).first()


def close_conversation(conversation_id: int):
    conversation = get_conversation_by_id(conversation_id)
    if conversation and conversation.IsOpen:
        conversation.IsOpen = False
        conversation.EndTime = datetime.utcnow()
        db.session.commit()
        return conversation
    return None


def update_conversation(conversation_id: int, **kwargs):
    conversation = get_conversation_by_id(conversation_id)
    if not conversation:
        return None
    for key, value in kwargs.items():
        if hasattr(conversation, key):
            setattr(conversation, key, value)
    db.session.commit()
    return conversation


def delete_conversation(conversation_id: int):
    conversation = get_conversation_by_id(conversation_id)
    if conversation:
        db.session.delete(conversation)
        db.session.commit()
        return True
    return False
