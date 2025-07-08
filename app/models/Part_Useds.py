from app import db
from sqlalchemy.orm import relationship

class PartsUsed(db.Model):  # دقت کنید نام کلاس با روابط یکسان باشد
    __tablename__ = 'partsused'

    PartsUsedID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RepairRequestID = db.Column(db.Integer, db.ForeignKey('repairrequests.RepairRequestID'), nullable=False)
    PartID = db.Column(db.Integer, db.ForeignKey('partsinventory.PartID'), nullable=False)
    QuantityUsed = db.Column(db.Integer, default=1)

    RepairRequest = relationship('RepairRequest', back_populates='PartsUsed')
    Part = relationship('PartInventory')

    def __repr__(self):
        return f"<PartsUsed {self.PartsUsedID} - PartID {self.PartID} Qty {self.QuantityUsed}>"
