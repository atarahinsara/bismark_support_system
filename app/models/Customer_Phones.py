from app import db

class CustomerPhone(db.Model):
    __tablename__ = 'customer_phones'

    PhoneID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PhoneNumber = db.Column(db.String(20), nullable=False, unique=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)
    PhoneType = db.Column(db.Enum('Mobile', 'Home', 'Work'), default='Mobile', nullable=True)

    customer = db.relationship("Customer", back_populates="phones")
 
    def __repr__(self):
        return f"<CustomerPhone {self.PhoneNumber} ({self.PhoneType})>"

# -----------------------------
# CRUD Functions for CustomerPhone
# -----------------------------
def create_customer_phone(customer_id, phone_number, phone_type="Mobile"):
    phone = CustomerPhone(
        PhoneNumber=phone_number,
        CustomerID=customer_id,
        PhoneType=phone_type
    )
    db.session.add(phone)
    db.session.commit()
    return phone

def get_customer_phone_by_id(phone_id):
    return CustomerPhone.query.get(phone_id)

def get_phones_by_customer(customer_id):
    return CustomerPhone.query.filter_by(CustomerID=customer_id).all()

def update_customer_phone(phone_id, **kwargs):
    phone = get_customer_phone_by_id(phone_id)
    if not phone:
        return None
    for key, value in kwargs.items():
        if hasattr(phone, key):
            setattr(phone, key, value)
    db.session.commit()
    return phone

def delete_customer_phone(phone_id):
    phone = get_customer_phone_by_id(phone_id)
    if phone:
        db.session.delete(phone)
        db.session.commit()
        return True
    return False
