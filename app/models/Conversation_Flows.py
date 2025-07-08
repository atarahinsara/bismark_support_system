# مسیر: app/models/conversation_flow.py

from app import db
from datetime import datetime

class ConversationFlow(db.Model):
    __tablename__ = 'conversation_flows'

    FlowID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PhoneNumber = db.Column(db.String(20), nullable=False, unique=True)
    Step = db.Column(db.String(50), nullable=False, default='full_name')
    TempData = db.Column(db.Text, nullable=True)  # JSON format
    LastUpdated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConversationFlow {self.PhoneNumber} - Step: {self.Step}>"
