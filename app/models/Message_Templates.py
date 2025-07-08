from app import db
from datetime import datetime

class MessageTemplate(db.Model):
    __tablename__ = 'message_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_type = db.Column(db.String(50), unique=True, nullable=False)  # Customer, SalesRep, Technician, Unknown
    message_template = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<MessageTemplate {self.sender_type}>"
