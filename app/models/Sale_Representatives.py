from app import db
from sqlalchemy.orm import relationship

class SalesRepresentative(db.Model):
    __tablename__ = 'salesrepresentatives'

    SalesRepID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    ShopAddress = db.Column(db.String(255))
    Province = db.Column(db.String(50))
    City = db.Column(db.String(50))
    IsActive = db.Column(db.Boolean, default=True)
    RegisterDate = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    GenderID = db.Column(db.Integer, db.ForeignKey('gender.GenderID'))
    Gender = relationship('Gender', backref='SalesRepresentatives')

    Phones = relationship('SalesRepresentativePhone', back_populates='SalesRepresentative', cascade="all, delete-orphan", lazy='selectin')

    def __repr__(self):
        return f"<SalesRepresentative {self.SalesRepID} - {self.FirstName} {self.LastName}>"
