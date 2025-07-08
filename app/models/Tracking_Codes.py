from app import db
from sqlalchemy.orm import relationship

class TrackingCode(db.Model):
    __tablename__ = 'trackingcodes'

    TrackingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Code = db.Column(db.String(50), unique=True, nullable=False)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=False)
    RequestDate = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    Status = db.Column(db.String(50), default='Pending')

    Customer = relationship('Customer', back_populates='TrackingCodes')
    Product = relationship('Product', back_populates='TrackingCodes')
    RepairRequests = relationship('RepairRequest', back_populates='TrackingCode', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<TrackingCode {self.TrackingID} - {self.Code}>"
