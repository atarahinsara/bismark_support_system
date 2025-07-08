# app/models/nlp/NLPKeyword.py
from app import db

class NLPKeyword(db.Model):
    __tablename__ = 'nlp_keywords_library'

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100), nullable=False)
    intent_id = db.Column(db.Integer, db.ForeignKey('nlp_intents.id'), nullable=False)

    intent = db.relationship('NLPIntent', back_populates='keywords')
