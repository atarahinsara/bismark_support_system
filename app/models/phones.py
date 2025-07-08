from app import db

class Phones(db.Model):
    __tablename__ = "phones"

    PhoneID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PhoneNumber = db.Column(db.String(20), nullable=False, unique=True)
    OwnerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)
    OwnerType = db.Column(db.String(20), nullable=False)  # مثلا 'Customer', 'SalesRep', 'Technician'

    def __repr__(self):
        return f"<Phone {self.PhoneNumber} Owner: {self.OwnerType}({self.OwnerID})>"
