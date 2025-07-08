from app import db
from sqlalchemy.orm import relationship

class Invoice(db.Model):
    __tablename__ = 'invoices'

    InvoiceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RepairRequestID = db.Column(db.Integer, db.ForeignKey('repairrequests.RepairRequestID'), nullable=False)
    TechnicianID = db.Column(db.Integer, db.ForeignKey('servicetechnicians.TechnicianID'), nullable=False)
    PartsCost = db.Column(db.Float, default=0)
    LaborCost = db.Column(db.Float, default=0)
    TotalCost = db.Column(db.Float, default=0)
    InvoiceDate = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    RepairRequest = relationship('RepairRequest', back_populates='Invoices')
    Technician = relationship('ServiceTechnician')

    def __repr__(self):
        return f"<Invoice {self.InvoiceID} - RepairRequest {self.RepairRequestID}>"
