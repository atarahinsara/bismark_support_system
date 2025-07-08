from app import db
from sqlalchemy.orm import relationship

class ServiceTechnician(db.Model):
    __tablename__ = 'servicetechnicians'

    TechnicianID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    ShopAddress = db.Column(db.String(255))
    Province = db.Column(db.String(50))
    City = db.Column(db.String(50))
    IsActive = db.Column(db.Boolean, default=True)
    RegisterDate = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    Rank = db.Column(db.Float, default=0)

    GenderID = db.Column(db.Integer, db.ForeignKey('gender.GenderID'))
    Gender = relationship('Gender', backref='ServiceTechnicians')

    Phones = relationship('TechnicianPhone', back_populates='Technician', cascade="all, delete-orphan", lazy='selectin')

    # اضافه کردن رابطه معکوس RepairRequests
    RepairRequests = relationship('RepairRequest', back_populates='Technician', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<ServiceTechnician {self.TechnicianID} - {self.FirstName} {self.LastName}>"
