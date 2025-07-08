# app/models/nlp/NLPIntent.py
from app import db

class NLPIntent(db.Model):
    __tablename__ = 'nlp_intents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    # رابطه معکوس برای دسترسی به کلمات کلیدی
    keywords = db.relationship('NLPKeyword', back_populates='intent', lazy='dynamic')
