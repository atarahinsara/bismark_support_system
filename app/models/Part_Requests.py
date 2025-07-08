from app import db
from sqlalchemy.orm import relationship

class PartRequest(db.Model):
    __tablename__ = 'partsrequests'

    PartsRequestID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RepairRequestID = db.Column(db.Integer, db.ForeignKey('repairrequests.RepairRequestID'), nullable=False)
    PartName = db.Column(db.String(100), nullable=False)
    Quantity = db.Column(db.Integer, default=1)
    IsApproved = db.Column(db.Boolean, default=False)
    RequestDate = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    ApprovalDate = db.Column(db.DateTime)

    RepairRequest = relationship('RepairRequest', back_populates='PartsRequests')

    def __repr__(self):
        return f"<PartRequest {self.PartsRequestID} - Part {self.PartName} Qty {self.Quantity}>"
