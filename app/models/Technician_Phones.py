from app import db
from sqlalchemy.orm import relationship

class TechnicianPhone(db.Model):
    __tablename__ = 'technician_phones'

    PhoneID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PhoneNumber = db.Column(db.String(20), nullable=False, unique=True)
    TechnicianID = db.Column(db.Integer, db.ForeignKey('servicetechnicians.TechnicianID'), nullable=False)
    PhoneType = db.Column(db.Enum('Mobile', 'Work'), default='Mobile')

    Technician = relationship('ServiceTechnician', back_populates='Phones')

    def __repr__(self):
        return f"<TechnicianPhone {self.PhoneNumber} ({self.PhoneType})>"