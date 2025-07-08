from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

class Gender(db.Model):
    __tablename__ = 'gender'

    GenderID = Column(Integer, primary_key=True, autoincrement=True)
    GenderName = Column(String(20), nullable=False)

    # اضافه کردن رابطه معکوس با Customer
    Customers = relationship('Customer', back_populates='Gender', lazy='selectin')

    def __repr__(self):
        return f"<Gender(GenderID={self.GenderID}, GenderName='{self.GenderName}')>"
