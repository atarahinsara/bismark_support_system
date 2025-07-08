from app import db
from datetime import datetime

class CustomerTemp(db.Model):
    __tablename__ = 'customers_Temp'

    TempID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False, unique=True)
    Province = db.Column(db.String(100), nullable=True)
    City = db.Column(db.String(100), nullable=True)
    Address = db.Column(db.Text, nullable=True)
    Status = db.Column(db.Enum('collecting', 'incomplete', 'complete'), default='collecting')
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<CustomersTemp {self.TempID} - {self.PhoneNumber}>"


# =====================
# متدهای CRUD
# =====================

def create_customers_temp(first_name, last_name, phone_number, province=None, city=None, address=None, status='collecting'):
    new_customer = CustomerTemp(
        first_name=first_name,
        last_name=last_name,
        PhoneNumber=phone_number,
        Province=province,
        City=city,
        Address=address,
        Status=status,
        CreatedAt=datetime.utcnow()
    )
    db.session.add(new_customer)
    db.session.commit()
    return new_customer


def get_customers_temp_by_id(temp_id):
    return CustomerTemp.query.get(temp_id)


def get_customers_temp_by_phone(phone_number):
    return CustomerTemp.query.filter_by(PhoneNumber=phone_number).first()


def update_customers_temp(temp_id, **kwargs):
    customer = get_customers_temp_by_id(temp_id)
    if not customer:
        return None
    for key, value in kwargs.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    db.session.commit()
    return customer


def delete_customers_temp(temp_id):
    customer = get_customers_temp_by_id(temp_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return True
    return False
