from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

class Message(db.Model):
    __tablename__ = 'messages'

    MessageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ConversationID = db.Column(db.Integer, db.ForeignKey('conversations.ConversationID'), nullable=False)
    SenderType = db.Column(db.Enum('Customer', 'SalesRep', 'Technician', 'System'), nullable=False)
    SenderID = db.Column(db.Integer)
    Content = db.Column(db.String(1000), nullable=False)
    Timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())

#    Conversation = relationship('Conversation', back_populates='Messages')

    def __repr__(self):
        return f"<Message {self.MessageID} from {self.SenderType}>"
