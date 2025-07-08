from app import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'

    CustomerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Province = db.Column(db.String(50), nullable=False)
    City = db.Column(db.String(50), nullable=False)
    Address = db.Column(db.String(255), nullable=True)
    RegisterDate = db.Column(db.DateTime, default=datetime.utcnow)
    GenderID = db.Column(db.Integer, db.ForeignKey('gender.GenderID'), nullable=True)

    # روابط فعلی
    phones = db.relationship('CustomerPhone', back_populates='customer', cascade="all, delete-orphan", lazy='joined')
    Products = db.relationship('Product', back_populates='Customer', cascade="all, delete-orphan", lazy='selectin')
    TrackingCodes = db.relationship('TrackingCode', back_populates='Customer', cascade="all, delete-orphan", lazy='selectin')
    Gender = db.relationship('Gender', back_populates='Customers', lazy='joined')

    # این رابطه را اضافه کن:
    RepairRequests = db.relationship('RepairRequest', back_populates='Customer', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer {self.CustomerID} - {self.FirstName} {self.LastName}>"

# -----------------------------
# CRUD Functions for Customer
# -----------------------------
def create_customer(first_name, last_name, province, city, address=None, gender_id=None):
    customer = Customer(
        FirstName=first_name,
        LastName=last_name,
        Province=province,
        City=city,
        Address=address,
        GenderID=gender_id
    )
    db.session.add(customer)
    db.session.commit()
    return customer

def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)

def get_all_customers():
    return Customer.query.all()

def update_customer(customer_id, **kwargs):
    customer = get_customer_by_id(customer_id)
    if not customer:
        return None
    for key, value in kwargs.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    db.session.commit()
    return customer

def delete_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return True
    return False
