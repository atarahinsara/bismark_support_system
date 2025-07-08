from app import db

class PartInventory(db.Model):
    __tablename__ = 'partsinventory'

    PartID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PartName = db.Column(db.String(100), unique=True, nullable=False)
    QuantityAvailable = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<PartsInventory {self.PartName} - {self.QuantityAvailable}>"
