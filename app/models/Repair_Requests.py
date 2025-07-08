from app import db
from sqlalchemy.orm import relationship

class RepairRequest(db.Model):
    __tablename__ = 'repairrequests'

    RepairRequestID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=False)
    Description = db.Column(db.String(1000), nullable=False)
    TrackingID = db.Column(db.Integer, db.ForeignKey('trackingcodes.TrackingID'), nullable=False)
    TechnicianID = db.Column(db.Integer, db.ForeignKey('servicetechnicians.TechnicianID'))
    RequestDate = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    IsCompleted = db.Column(db.Boolean, default=False)

    Customer = relationship('Customer', back_populates='RepairRequests')
    Product = relationship('Product', back_populates='RepairRequests')
    TrackingCode = relationship('TrackingCode', back_populates='RepairRequests')
    Technician = relationship('ServiceTechnician', back_populates='RepairRequests')

    PartsRequests = relationship('PartRequest', back_populates='RepairRequest', cascade='all, delete-orphan')
    PartsUsed = relationship('PartsUsed', back_populates='RepairRequest', cascade='all, delete-orphan')
    Invoices = relationship('Invoice', back_populates='RepairRequest', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<RepairRequest {self.RepairRequestID} - Customer {self.CustomerID}>"
