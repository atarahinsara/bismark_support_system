from app import db
from sqlalchemy.orm import relationship

class SalesRepresentativePhone(db.Model):
    __tablename__ = 'sales_rep_phones'

    PhoneID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PhoneNumber = db.Column(db.String(20), nullable=False, unique=True)
    SalesRepID = db.Column(db.Integer, db.ForeignKey('salesrepresentatives.SalesRepID'), nullable=False)
    PhoneType = db.Column(db.Enum('Mobile', 'Work'), default='Mobile')

    SalesRepresentative = relationship('SalesRepresentative', back_populates='Phones')

    def __repr__(self):
        return f"<SalesRepresentativePhone {self.PhoneNumber} ({self.PhoneType})>"