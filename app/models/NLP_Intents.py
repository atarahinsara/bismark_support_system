from app import db

class NLPIntent(db.Model):
    __tablename__ = 'nlpintents'

    IntentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), unique=True, nullable=False)
    Description = db.Column(db.Text)

    def __repr__(self):
        return f"<NlpIntent {self.Name}>"
