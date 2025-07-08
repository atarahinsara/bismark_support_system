from app import db

class NLPInvalidInput(db.Model):
    __tablename__ = 'nlp_invalid_inputs'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    received_at = db.Column(db.DateTime, server_default=db.func.now())
