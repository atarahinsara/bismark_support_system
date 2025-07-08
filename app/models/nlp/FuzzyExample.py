from app import db

class NLPFuzzyMatch(db.Model):
    __tablename__ = 'nlp_fuzzy_matches'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    intent_id = db.Column(db.Integer, db.ForeignKey('nlp_intents.id'), nullable=False)
    intent = db.relationship('NLPIntent', backref='examples')
