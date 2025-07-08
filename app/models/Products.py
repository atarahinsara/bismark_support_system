from app import db
from sqlalchemy.orm import relationship

# مدل Product (همانطور که شما داری)
class Product(db.Model):
    __tablename__ = 'products'

    ProductID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)
    ProductCode = db.Column(db.String(50), nullable=False)
    Brand = db.Column(db.String(50))
    Model = db.Column(db.String(100))
    SerialNumber = db.Column(db.String(100))
    WarrantyCardNumber = db.Column(db.String(100))
    PurchaseDate = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    Customer = relationship('Customer', back_populates='Products')
    TrackingCodes = relationship('TrackingCode', back_populates='Product', cascade='all, delete-orphan')
    RepairRequests = relationship('RepairRequest', back_populates='Product', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Product {self.ProductID} - {self.ProductCode}>"
